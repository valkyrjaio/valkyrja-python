#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import sys
from copy import copy
from typing import Self, cast, override

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.writer.contract.writer_contract import WriterContract
from valkyrja.cli.interaction.writer.question_writer import QuestionWriter


class Output(OutputContract):
    """The output that a command writes to."""

    def __init__(
        self,
        is_interactive: bool = True,
        is_quiet: bool = False,
        is_silent: bool = False,
        exit_code: ExitCode | int = ExitCode.SUCCESS,
        *messages: MessageContract,
    ) -> None:
        self._is_interactive = is_interactive
        self._is_quiet = is_quiet
        self._is_silent = is_silent
        self._exit_code = exit_code
        self._unwritten_messages: list[MessageContract] = list(messages)
        self._written_messages: list[MessageContract] = []
        self._writers: list[WriterContract] = [QuestionWriter()]

    @override
    def get_messages(self) -> list[MessageContract]:
        return [*self._written_messages, *self._unwritten_messages]

    @override
    def get_written_messages(self) -> list[MessageContract]:
        return list(self._written_messages)

    @override
    def has_written_message(self) -> bool:
        return self._written_messages != []

    @override
    def get_unwritten_messages(self) -> list[MessageContract]:
        return list(self._unwritten_messages)

    @override
    def has_unwritten_message(self) -> bool:
        return self._unwritten_messages != []

    @override
    def with_messages(self, *messages: MessageContract) -> Self:
        new = self._copy()
        new._unwritten_messages = list(messages)

        return new

    @override
    def with_added_messages(self, *messages: MessageContract) -> Self:
        new = self._copy()
        new._unwritten_messages = [*new._unwritten_messages, *messages]

        return new

    @override
    def with_added_message(self, message: MessageContract) -> Self:
        return self.with_added_messages(message)

    @override
    def write_messages(self) -> Self:
        new = self._copy()
        # Read the list first, then empty it. A writer can call `write_messages`
        # again inside the loop, and an emptied list stops the same message from
        # being written twice.
        unwritten = new._unwritten_messages
        new._unwritten_messages = []

        for message in unwritten:
            new = new._write_message_via_writer(message)

        return new

    @override
    def write_message(self, message: MessageContract) -> Self:
        self._written_messages.append(message)

        if self._is_silent or (self._is_quiet and self._exit_code == ExitCode.SUCCESS):
            return self

        self._output_message(message)

        return self

    @override
    def get_writers(self) -> list[WriterContract]:
        return list(self._writers)

    @override
    def with_writers(self, *writers: WriterContract) -> Self:
        new = self._copy()
        new._writers = list(writers)

        return new

    @override
    def is_interactive(self) -> bool:
        return self._is_interactive

    @override
    def with_is_interactive(self, is_interactive: bool) -> Self:
        new = self._copy()
        new._is_interactive = is_interactive

        return new

    @override
    def is_quiet(self) -> bool:
        return self._is_quiet

    @override
    def with_is_quiet(self, is_quiet: bool) -> Self:
        new = self._copy()
        new._is_quiet = is_quiet

        return new

    @override
    def is_silent(self) -> bool:
        return self._is_silent

    @override
    def with_is_silent(self, is_silent: bool) -> Self:
        new = self._copy()
        new._is_silent = is_silent

        return new

    @override
    def get_exit_code(self) -> ExitCode | int:
        return self._exit_code

    @override
    def with_exit_code(self, exit_code: ExitCode | int) -> Self:
        new = self._copy()
        new._exit_code = exit_code

        return new

    def _copy(self) -> Self:
        """Get a copy that holds its own message lists."""
        new = copy(self)
        new._unwritten_messages = list(self._unwritten_messages)
        new._written_messages = list(self._written_messages)
        new._writers = list(self._writers)

        return new

    def _write_message_via_writer(self, message: MessageContract) -> Self:
        """Give the message to the first writer that takes it."""
        for writer in self._writers:
            if writer.should_write_message(message):
                # A writer answers with the contract. Every writer answers with
                # the output that it received, so the concrete type is this one.
                return cast("Self", writer.write(self, message))

        return self.write_message(message)

    def _output_message(self, message: MessageContract) -> None:
        """Put the message where a reader sees it."""
        sys.stdout.write(message.get_formatted_text())
