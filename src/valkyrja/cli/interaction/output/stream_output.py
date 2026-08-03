#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, TextIO, override

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.output.contract.stream_output_contract import StreamOutputContract
from valkyrja.cli.interaction.output.output import Output


class StreamOutput(Output, StreamOutputContract):
    """An output that writes to a stream."""

    def __init__(
        self,
        stream: TextIO,
        is_interactive: bool = True,
        is_quiet: bool = False,
        is_silent: bool = False,
        exit_code: ExitCode | int = ExitCode.SUCCESS,
        *messages: MessageContract,
    ) -> None:
        super().__init__(is_interactive, is_quiet, is_silent, exit_code, *messages)

        self._stream = stream

    @override
    def get_stream(self) -> TextIO:
        return self._stream

    @override
    def with_stream(self, stream: TextIO) -> Self:
        new = copy(self)
        new._stream = stream

        return new

    @override
    def _output_message(self, message: MessageContract) -> None:
        self._stream.write(message.get_formatted_text())
