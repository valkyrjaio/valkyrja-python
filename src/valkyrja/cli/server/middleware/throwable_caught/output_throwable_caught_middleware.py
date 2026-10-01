#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from traceback import format_tb
from types import TracebackType
from typing import override

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.message.banner import Banner
from valkyrja.cli.interaction.message.error_message import ErrorMessage
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.message.new_line import NewLine
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.contract.throwable_caught_middleware_contract import (
    ThrowableCaughtMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)


class OutputThrowableCaughtMiddleware(ThrowableCaughtMiddlewareContract):
    @override
    def throwable_caught(
        self,
        input_: InputContract,
        output: OutputContract,
        throwable: BaseException,
        handler: ThrowableCaughtHandlerContract,
    ) -> OutputContract:
        command_name = input_.get_command_name()
        output = output.with_exit_code(ExitCode.ERROR).with_messages(
            Banner(ErrorMessage("Cli Server Error:")),
            NewLine(),
            ErrorMessage("Command:"),
            Message(f" {command_name}"),
            NewLine(),
            NewLine(),
            ErrorMessage("Message:"),
            Message(f" {throwable}"),
            NewLine(),
            NewLine(),
            ErrorMessage("Line:"),
            Message(f" {self._get_line(throwable)}"),
            NewLine(),
            NewLine(),
            ErrorMessage("Trace:"),
            NewLine(),
            Message(f"{self._get_trace(throwable)}\n"),
        )

        # The stage continues, so a middleware after this one reads the report.
        return handler.throwable_caught(input_, output, throwable)

    @staticmethod
    def _get_line(throwable: BaseException) -> int:
        """Get the line that raised, which PHP reads from `getLine`.

        The walk ends at the deepest frame, because that frame holds the raise. An
        unraised throwable carries no traceback, and it reports line zero.
        """
        line = 0
        traceback_: TracebackType | None = throwable.__traceback__

        while traceback_ is not None:
            line = traceback_.tb_lineno
            traceback_ = traceback_.tb_next

        return line

    @staticmethod
    def _get_trace(throwable: BaseException) -> str:
        """Get the trace, which PHP reads from `getTraceAsString`."""
        return "".join(format_tb(throwable.__traceback__)).rstrip("\n")
