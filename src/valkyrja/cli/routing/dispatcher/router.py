#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.message.banner import Banner
from valkyrja.cli.interaction.message.error_message import ErrorMessage
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.factory.contract.output_factory_contract import (
    OutputFactoryContract,
)
from valkyrja.cli.middleware.handler.contract.process_exiting_handler_contract import (
    ProcessExitingHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_dispatched_handler_contract import (
    RouteDispatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_matched_handler_contract import (
    RouteMatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_not_matched_handler_contract import (
    RouteNotMatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)
from valkyrja.cli.routing.collection.contract.route_collection_contract import (
    RouteCollectionContract,
)
from valkyrja.cli.routing.constant.cli_routing_service_id import CliRoutingServiceId
from valkyrja.cli.routing.data.contract.argument_parameter_contract import (
    ArgumentParameterContract,
)
from valkyrja.cli.routing.data.contract.option_parameter_contract import OptionParameterContract
from valkyrja.cli.routing.data.contract.route_contract import RouteContract
from valkyrja.cli.routing.dispatcher.contract.router_contract import RouterContract
from valkyrja.cli.routing.enum.argument_value_mode import ArgumentValueMode
from valkyrja.container.manager.contract.container_contract import ContainerContract


class Router(RouterContract):
    """Matches a command to the input, then answers it."""

    def __init__(
        self,
        container: ContainerContract,
        collection: RouteCollectionContract,
        output_factory: OutputFactoryContract,
        throwable_caught_handler: ThrowableCaughtHandlerContract,
        route_matched_handler: RouteMatchedHandlerContract,
        route_not_matched_handler: RouteNotMatchedHandlerContract,
        route_dispatched_handler: RouteDispatchedHandlerContract,
        process_exiting_handler: ProcessExitingHandlerContract,
    ) -> None:
        self._container = container
        self._collection = collection
        self._output_factory = output_factory
        self._throwable_caught_handler = throwable_caught_handler
        self._route_matched_handler = route_matched_handler
        self._route_not_matched_handler = route_not_matched_handler
        self._route_dispatched_handler = route_dispatched_handler
        self._process_exiting_handler = process_exiting_handler

    @override
    def dispatch(self, input_: InputContract) -> OutputContract:
        matched = self._attempt_to_match_route(input_)

        if isinstance(matched, OutputContract):
            return self._route_not_matched_handler.route_not_matched(input_, matched)

        return self.dispatch_route(input_, matched)

    @override
    def dispatch_route(self, input_: InputContract, route: RouteContract) -> OutputContract:
        route = self._add_parameters_to_route(input_, route)

        self._route_matched(route)

        after_middleware = self._route_matched_handler.route_matched(input_, route)

        if isinstance(after_middleware, OutputContract):
            return after_middleware

        # The middleware can replace the route, so the container holds the route
        # that the handler actually runs.
        self._container.set_singleton(CliRoutingServiceId.ROUTE_CONTRACT, after_middleware)

        handler = after_middleware.get_handler()
        # The handler reads the route from the container, never from the
        # signature. The second argument carries the arguments alone.
        output = handler(self._container, {})

        return self._route_dispatched_handler.route_dispatched(input_, output, after_middleware)

    def _attempt_to_match_route(self, input_: InputContract) -> RouteContract | OutputContract:
        """Get the command that the input names, or an output that reports none."""
        command_name = input_.get_command_name()

        if self._collection.has(command_name):
            return self._collection.get(command_name)

        return self._output_factory.create_output(exit_code=ExitCode.ERROR).with_messages(
            Banner(ErrorMessage(f"Command `{command_name}` was not found."))
        )

    def _route_matched(self, route: RouteContract) -> None:
        """Schedule the middleware of the route, and publish the route."""
        self._route_matched_handler.add(*route.get_route_matched_middleware())
        self._route_dispatched_handler.add(*route.get_route_dispatched_middleware())
        self._throwable_caught_handler.add(*route.get_throwable_caught_middleware())
        self._process_exiting_handler.add(*route.get_process_exiting_middleware())

        self._container.set_singleton(CliRoutingServiceId.ROUTE_CONTRACT, route)

    def _add_parameters_to_route(self, input_: InputContract, route: RouteContract) -> RouteContract:
        """Fill each parameter of the route from the input."""
        return self._add_options_to_route(input_, self._add_arguments_to_route(input_, route))

    def _add_arguments_to_route(self, input_: InputContract, route: RouteContract) -> RouteContract:
        """Give each argument of the input to the parameter that takes it."""
        arguments = list(input_.get_arguments())
        parameters: list[ArgumentParameterContract] = []

        for parameter in route.get_arguments():
            taken = []

            if parameter.get_value_mode() is ArgumentValueMode.ARRAY:
                taken = arguments
                arguments = []
            elif arguments:
                taken = [arguments.pop(0)]

            parameters.append(parameter.with_arguments(*taken).validate_values())

        return route.with_arguments(*parameters)

    def _add_options_to_route(self, input_: InputContract, route: RouteContract) -> RouteContract:
        """Give each option of the input to the parameter that takes it."""
        options = input_.get_options()
        parameters: list[OptionParameterContract] = []

        for parameter in route.get_options():
            taken = [
                option
                for option in options
                if option.get_name() == parameter.get_name() or option.get_name() in parameter.get_short_names()
            ]

            parameters.append(parameter.with_options(*taken).validate_values())

        return route.with_options(*parameters)
