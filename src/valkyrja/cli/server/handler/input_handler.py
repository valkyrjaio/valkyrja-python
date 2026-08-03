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
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.message.new_line import NewLine
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.factory.contract.output_factory_contract import (
    OutputFactoryContract,
)
from valkyrja.cli.middleware.handler.contract.input_received_handler_contract import (
    InputReceivedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.process_exiting_handler_contract import (
    ProcessExitingHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)
from valkyrja.cli.routing.dispatcher.contract.router_contract import RouterContract
from valkyrja.cli.server.constant.cli_server_service_id import CliServerServiceId
from valkyrja.cli.server.handler.contract.input_handler_contract import InputHandlerContract
from valkyrja.cli.server.support.exiter import Exiter
from valkyrja.container.manager.contract.container_contract import ContainerContract


class InputHandler(InputHandlerContract):
    """Answers one run of the program, from the input to the exit code."""

    def __init__(
        self,
        container: ContainerContract,
        router: RouterContract,
        input_received_handler: InputReceivedHandlerContract,
        throwable_caught_handler: ThrowableCaughtHandlerContract,
        process_exiting_handler: ProcessExitingHandlerContract,
        output_factory: OutputFactoryContract,
    ) -> None:
        self._container = container
        self._router = router
        self._input_received_handler = input_received_handler
        self._throwable_caught_handler = throwable_caught_handler
        self._process_exiting_handler = process_exiting_handler
        self._output_factory = output_factory

    @override
    def handle(self, input_: InputContract) -> OutputContract:
        try:
            output = self._dispatch_router(input_)
        except Exception as throwable:
            output = self._get_output_from_throwable(input_, throwable)
            output = self._throwable_caught_handler.throwable_caught(input_, output, throwable)

        self._container.set_singleton(CliServerServiceId.OUTPUT_CONTRACT, output)

        return output

    @override
    def exit(self, input_: InputContract, output: OutputContract) -> None:
        self._process_exiting_handler.process_exiting(input_, output)

    @override
    def run(self, input_: InputContract) -> None:
        output = self.handle(input_)

        output.write_messages()

        self.exit(input_, output)

        exit_code = output.get_exit_code()

        Exiter.exit(exit_code.value if isinstance(exit_code, ExitCode) else exit_code)

    def _dispatch_router(self, input_: InputContract) -> OutputContract:
        """Run the input received middleware, then give the input to the router."""
        self._container.set_singleton(CliServerServiceId.INPUT_CONTRACT, input_)

        after_middleware = self._input_received_handler.input_received(input_)

        if isinstance(after_middleware, OutputContract):
            return after_middleware

        self._container.set_singleton(CliServerServiceId.INPUT_CONTRACT, after_middleware)

        return self._router.dispatch(after_middleware)

    def _get_output_from_throwable(self, input_: InputContract, throwable: BaseException) -> OutputContract:
        """Build the output that reports a throwable to the user."""
        return self._output_factory.create_output(ExitCode.ERROR).with_messages(
            Banner(ErrorMessage("Cli Server Error:")),
            NewLine(),
            ErrorMessage("Command:"),
            Message(f" {input_.get_command_name()}"),
            NewLine(),
            NewLine(),
            ErrorMessage("Message:"),
            Message(f" {throwable}"),
        )
