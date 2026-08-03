#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.routing.data.contract.argument_parameter_contract import (
    ArgumentParameterContract,
)
from valkyrja.cli.routing.data.contract.option_parameter_contract import OptionParameterContract
from valkyrja.cli.routing.data.contract.route_contract import CliHandler, HelpText, RouteContract
from valkyrja.cli.routing.throwable.exception.cli_routing_invalid_argument_name_exception import (
    CliRoutingInvalidArgumentNameException,
)
from valkyrja.cli.routing.throwable.exception.cli_routing_invalid_option_name_exception import (
    CliRoutingInvalidOptionNameException,
)
from valkyrja.cli.routing.throwable.exception.cli_routing_no_help_text_exception import (
    CliRoutingNoHelpTextException,
)


class Route(RouteContract):
    """One command that the application answers.

    PHP checks that the help text is a callable array, so `sindri` can read it
    from the source. Python has no such shape: a plain function reference is
    what `sindri` reads through the abstract syntax tree, so this port carries
    no equivalent check.
    """

    def __init__(
        self,
        name: str,
        description: str,
        handler: CliHandler,
        help_text: HelpText | None = None,
        route_matched_middleware: list[str] | None = None,
        route_dispatched_middleware: list[str] | None = None,
        throwable_caught_middleware: list[str] | None = None,
        process_exiting_middleware: list[str] | None = None,
        arguments: list[ArgumentParameterContract] | None = None,
        options: list[OptionParameterContract] | None = None,
    ) -> None:
        self._name = name
        self._description = description
        self._handler = handler
        self._help_text = help_text
        self._route_matched_middleware: list[str] = (
            list(route_matched_middleware) if route_matched_middleware is not None else []
        )
        self._route_dispatched_middleware: list[str] = (
            list(route_dispatched_middleware) if route_dispatched_middleware is not None else []
        )
        self._throwable_caught_middleware: list[str] = (
            list(throwable_caught_middleware) if throwable_caught_middleware is not None else []
        )
        self._process_exiting_middleware: list[str] = (
            list(process_exiting_middleware) if process_exiting_middleware is not None else []
        )
        self._arguments: list[ArgumentParameterContract] = list(arguments) if arguments is not None else []
        self._options: list[OptionParameterContract] = list(options) if options is not None else []

    @override
    def get_name(self) -> str:
        return self._name

    @override
    def with_name(self, name: str) -> Self:
        new = self._copy()
        new._name = name

        return new

    @override
    def get_description(self) -> str:
        return self._description

    @override
    def with_description(self, description: str) -> Self:
        new = self._copy()
        new._description = description

        return new

    @override
    def has_help_text(self) -> bool:
        return self._help_text is not None

    @override
    def get_help_text(self) -> HelpText:
        if self._help_text is None:
            raise CliRoutingNoHelpTextException("No help text exists")

        return self._help_text

    @override
    def get_help_text_message(self) -> MessageContract:
        return self.get_help_text()()

    @override
    def with_help_text(self, help_text: HelpText) -> Self:
        new = self._copy()
        new._help_text = help_text

        return new

    @override
    def has_arguments(self) -> bool:
        return self._arguments != []

    @override
    def get_arguments(self) -> list[ArgumentParameterContract]:
        return list(self._arguments)

    @override
    def has_argument(self, name: str) -> bool:
        return self._filter_arguments_by_name(name) != []

    @override
    def get_argument(self, name: str) -> ArgumentParameterContract:
        arguments = self._filter_arguments_by_name(name)

        if not arguments:
            raise CliRoutingInvalidArgumentNameException(f"The argument `{name}` was not found")

        return arguments[0]

    @override
    def with_arguments(self, *arguments: ArgumentParameterContract) -> Self:
        new = self._copy()
        new._arguments = list(arguments)

        return new

    @override
    def with_added_arguments(self, *arguments: ArgumentParameterContract) -> Self:
        new = self._copy()
        new._arguments = [*new._arguments, *arguments]

        return new

    @override
    def has_options(self) -> bool:
        return self._options != []

    @override
    def get_options(self) -> list[OptionParameterContract]:
        return list(self._options)

    @override
    def has_option(self, name: str) -> bool:
        return self._filter_options_by_name(name) != []

    @override
    def get_option(self, name: str) -> OptionParameterContract:
        options = self._filter_options_by_name(name)

        if not options:
            raise CliRoutingInvalidOptionNameException(f"The option `{name}` was not found")

        return options[0]

    @override
    def with_options(self, *options: OptionParameterContract) -> Self:
        new = self._copy()
        new._options = list(options)

        return new

    @override
    def with_added_options(self, *options: OptionParameterContract) -> Self:
        new = self._copy()
        new._options = [*new._options, *options]

        return new

    @override
    def get_route_matched_middleware(self) -> list[str]:
        return list(self._route_matched_middleware)

    @override
    def with_route_matched_middleware(self, *middleware: str) -> Self:
        new = self._copy()
        new._route_matched_middleware = list(middleware)

        return new

    @override
    def with_added_route_matched_middleware(self, *middleware: str) -> Self:
        new = self._copy()
        new._route_matched_middleware = [*new._route_matched_middleware, *middleware]

        return new

    @override
    def get_route_dispatched_middleware(self) -> list[str]:
        return list(self._route_dispatched_middleware)

    @override
    def with_route_dispatched_middleware(self, *middleware: str) -> Self:
        new = self._copy()
        new._route_dispatched_middleware = list(middleware)

        return new

    @override
    def with_added_route_dispatched_middleware(self, *middleware: str) -> Self:
        new = self._copy()
        new._route_dispatched_middleware = [*new._route_dispatched_middleware, *middleware]

        return new

    @override
    def get_throwable_caught_middleware(self) -> list[str]:
        return list(self._throwable_caught_middleware)

    @override
    def with_throwable_caught_middleware(self, *middleware: str) -> Self:
        new = self._copy()
        new._throwable_caught_middleware = list(middleware)

        return new

    @override
    def with_added_throwable_caught_middleware(self, *middleware: str) -> Self:
        new = self._copy()
        new._throwable_caught_middleware = [*new._throwable_caught_middleware, *middleware]

        return new

    @override
    def get_process_exiting_middleware(self) -> list[str]:
        return list(self._process_exiting_middleware)

    @override
    def with_process_exiting_middleware(self, *middleware: str) -> Self:
        new = self._copy()
        new._process_exiting_middleware = list(middleware)

        return new

    @override
    def with_added_process_exiting_middleware(self, *middleware: str) -> Self:
        new = self._copy()
        new._process_exiting_middleware = [*new._process_exiting_middleware, *middleware]

        return new

    @override
    def get_handler(self) -> CliHandler:
        return self._handler

    @override
    def with_handler(self, handler: CliHandler) -> Self:
        new = self._copy()
        new._handler = handler

        return new

    def _filter_arguments_by_name(self, name: str) -> list[ArgumentParameterContract]:
        """Get each argument that carries a given name."""
        return [argument for argument in self._arguments if argument.get_name() == name]

    def _filter_options_by_name(self, name: str) -> list[OptionParameterContract]:
        """Get each option that carries a given name, by name or by short name."""
        return [option for option in self._options if option.get_name() == name or name in option.get_short_names()]

    def _copy(self) -> Self:
        """Get a copy that holds its own lists."""
        new = copy(self)
        new._arguments = list(self._arguments)
        new._options = list(self._options)
        new._route_matched_middleware = list(self._route_matched_middleware)
        new._route_dispatched_middleware = list(self._route_dispatched_middleware)
        new._throwable_caught_middleware = list(self._throwable_caught_middleware)
        new._process_exiting_middleware = list(self._process_exiting_middleware)

        return new
