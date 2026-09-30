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
from valkyrja.cli.interaction.throwable.exception.cli_interaction_stream_write_exception import (
    CliInteractionStreamWriteException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_unwritable_stream_exception import (
    CliInteractionUnwritableStreamException,
)


class StreamOutput(Output, StreamOutputContract):
    def __init__(
        self,
        stream: TextIO,
        *messages: MessageContract,
        is_interactive: bool = True,
        is_quiet: bool = False,
        is_silent: bool = False,
        exit_code: ExitCode | int = ExitCode.SUCCESS,
    ) -> None:
        super().__init__(
            *messages,
            is_interactive=is_interactive,
            is_quiet=is_quiet,
            is_silent=is_silent,
            exit_code=exit_code,
        )

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
        self._verify_writable()

        data = message.get_formatted_text()
        offset = 0

        # A short write is not a failure. A non-blocking stream takes a long message
        # over several calls, so the loop offers the rest while the stream takes part.
        while offset < len(data):
            try:
                written = self._stream.write(data[offset:])
            except (OSError, ValueError) as exception:
                raise CliInteractionStreamWriteException(
                    f"Unable to write the whole message to the stream: {exception}"
                ) from exception

            if written == 0:
                raise CliInteractionStreamWriteException(
                    "Unable to write the whole message to the stream: the stream took no character of the offer"
                )

            offset += written

    def _verify_writable(self) -> None:
        """Check that the stream takes a write.

        A closed stream and a stream open in a read mode both report a failure the
        write cannot name, so this check names the condition instead.
        """
        if self._stream.closed:
            raise CliInteractionUnwritableStreamException("The stream is closed")

        if not self._stream.writable():
            raise CliInteractionUnwritableStreamException("The stream mode takes no write")
