#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.cli.interaction.constant.cli_interaction_service_id import (
    CliInteractionServiceId,
)
from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.message.banner import Banner
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.message.error_message import ErrorMessage
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.message.new_line import NewLine
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.factory.contract.output_factory_contract import (
    OutputFactoryContract,
)
from valkyrja.cli.interaction.output.output import Output
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
from valkyrja.cli.server.handler.contract.input_handler_contract import InputHandlerContract
from valkyrja.cli.server.support.exiter import Exiter
from valkyrja.container.manager.contract.container_contract import ContainerContract


class InputHandler(InputHandlerContract):
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
            try:
                # A middleware runs here, so the dispatch belongs under a guard of its own.
                output = self._get_output_from_throwable(input_, throwable)
                output = self._throwable_caught_handler.throwable_caught(input_, output, throwable)
            except Exception as recovery_throwable:
                output = self._get_recovery_output(input_, throwable, recovery_throwable)

        self._container.set_singleton(CliInteractionServiceId.OUTPUT_CONTRACT, output)

        return output

    @override
    def exit(self, input_: InputContract, output: OutputContract) -> None:
        self._process_exiting_handler.process_exiting(input_, output)

    @override
    def run(self, input_: InputContract) -> None:
        output = self.handle(input_)

        try:
            output = output.write_messages()

            self._container.set_singleton(CliInteractionServiceId.OUTPUT_CONTRACT, output)
        except Exception as throwable:
            try:
                # A middleware runs here, so the dispatch belongs under the same guard as
                # the write.
                output = self._get_output_from_throwable(input_, throwable)
                output = self._throwable_caught_handler.throwable_caught(input_, output, throwable)
                output = output.write_messages()
            except Exception as recovery_throwable:
                # The build of the first report, the dispatch, or the write of the output
                # the stage returned failed. That output can hold the destination that
                # just failed.
                output = self._get_recovery_output(input_, throwable, recovery_throwable)
                output = output.write_messages()

            self._container.set_singleton(CliInteractionServiceId.OUTPUT_CONTRACT, output)

        try:
            self.exit(input_, output)
        except Exception as exit_throwable:
            try:
                # The exit stage runs a middleware, and the run still ends through the
                # exiter, so this report is the only trace the failure leaves.
                self._get_output_from_throwable(input_, exit_throwable).write_messages()
            except Exception as report_throwable:
                self._get_recovery_output(input_, exit_throwable, report_throwable).write_messages()

        Exiter.exit(self._get_exit_code(input_, output))

    def _dispatch_router(self, input_: InputContract) -> OutputContract:
        """Run the input received middleware, then give the input to the router."""
        self._container.set_singleton(CliInteractionServiceId.INPUT_CONTRACT, input_)

        after_middleware = self._input_received_handler.input_received(input_)

        if isinstance(after_middleware, OutputContract):
            return after_middleware

        self._container.set_singleton(CliInteractionServiceId.INPUT_CONTRACT, after_middleware)

        return self._router.dispatch(after_middleware)

    def _get_output_from_throwable(self, input_: InputContract, throwable: BaseException) -> OutputContract:
        """Build the output that reports a throwable to the user."""
        return self._output_factory.create_output(exit_code=ExitCode.ERROR).with_messages(
            *self._get_throwable_messages(input_, throwable)
        )

    def _get_exit_code(self, input_: InputContract, output: OutputContract) -> int:
        """Get the code the output ends the process with.

        An output supplies this value, and an implementation of the contract can
        raise on the read. The code must reach the shell either way.
        """
        try:
            exit_code = output.get_exit_code()
        except Exception as code_throwable:
            # This read runs last, so the report is the only trace the failure leaves.
            self._get_recovery_output(input_, code_throwable).write_messages()

            return ExitCode.ERROR.value

        return exit_code.value if isinstance(exit_code, ExitCode) else exit_code

    def _get_recovery_output(
        self,
        input_: InputContract,
        throwable: BaseException,
        recovery_throwable: BaseException | None = None,
    ) -> OutputContract:
        """Get the output that reports a throwable, and one a recovery raised.

        A first report goes through the `OutputFactory`, so a silent run suppresses
        it. This recovery report takes an `Output` that this handler builds, which no
        configured factory redirects and no flag suppresses. Every unguarded write of
        this output rests on that, so this method and the messages it builds take no
        override.
        """
        recovery_messages = self._get_recovery_messages(recovery_throwable) if recovery_throwable is not None else []

        try:
            messages = [*self._get_throwable_messages(input_, throwable), *recovery_messages]
        except Exception:
            # The first report reads the command name from the input, so an input that
            # raises there takes the report with it.
            messages = [*self._get_bare_throwable_messages(throwable), *recovery_messages]

        return Output(exit_code=ExitCode.ERROR).with_messages(*messages)

    @staticmethod
    def _get_recovery_messages(recovery_throwable: BaseException) -> list[MessageContract]:
        """Get the messages that report the throwable a recovery raised."""
        return [
            NewLine(),
            ErrorMessage("Recovery message:"),
            Message(f" {recovery_throwable}"),
            NewLine(),
        ]

    @staticmethod
    def _get_bare_throwable_messages(throwable: BaseException) -> list[MessageContract]:
        """Get the messages that report one throwable without reading the input."""
        return [
            Banner(ErrorMessage("Cli Server Error:")),
            NewLine(),
            ErrorMessage("Message:"),
            Message(f" {throwable}"),
            NewLine(),
        ]

    @staticmethod
    def _get_throwable_messages(input_: InputContract, throwable: BaseException) -> list[MessageContract]:
        """Get the messages that report a throwable."""
        command_name = input_.get_command_name()

        return [
            Banner(ErrorMessage("Cli Server Error:")),
            NewLine(),
            ErrorMessage("Command:"),
            Message(f" {command_name}"),
            NewLine(),
            NewLine(),
            ErrorMessage("Message:"),
            Message(f" {throwable}"),
            # The report ends the line it wrote, so the shell prompt does not land on it.
            NewLine(),
        ]
