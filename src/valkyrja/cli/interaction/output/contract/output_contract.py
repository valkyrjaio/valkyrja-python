#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.writer.contract.writer_contract import WriterContract


class OutputContract(ABC):
    """The contract for the output that a command writes to."""

    @abstractmethod
    def get_messages(self) -> list[MessageContract]:
        """Get each message, with the written messages before the unwritten ones."""

    @abstractmethod
    def get_written_messages(self) -> list[MessageContract]:
        """Get each message that the output wrote already."""

    @abstractmethod
    def has_written_message(self) -> bool:
        """Get whether the output wrote a message already."""

    @abstractmethod
    def get_unwritten_messages(self) -> list[MessageContract]:
        """Get each message that the output holds but did not write."""

    @abstractmethod
    def has_unwritten_message(self) -> bool:
        """Get whether the output holds a message that it did not write."""

    @abstractmethod
    def with_messages(self, *messages: MessageContract) -> Self:
        """Get a copy of the output that holds different messages."""

    @abstractmethod
    def with_added_messages(self, *messages: MessageContract) -> Self:
        """Get a copy of the output that holds more messages."""

    @abstractmethod
    def with_added_message(self, message: MessageContract) -> Self:
        """Get a copy of the output that holds one more message."""

    @abstractmethod
    def write_messages(self) -> Self:
        """Write each message that the output did not write."""

    @abstractmethod
    def write_message(self, message: MessageContract) -> Self:
        """Write one message."""

    @abstractmethod
    def get_writers(self) -> list[WriterContract]:
        """Get each writer that the output uses."""

    @abstractmethod
    def with_writers(self, *writers: WriterContract) -> Self:
        """Get a copy of the output that uses different writers."""

    @abstractmethod
    def is_interactive(self) -> bool:
        """Get whether the output asks a question of the user."""

    @abstractmethod
    def with_is_interactive(self, is_interactive: bool) -> Self:
        """Get a copy of the output that records whether it asks a question."""

    @abstractmethod
    def is_quiet(self) -> bool:
        """Get whether the output drops a message of low importance."""

    @abstractmethod
    def with_is_quiet(self, is_quiet: bool) -> Self:
        """Get a copy of the output that records whether it is quiet."""

    @abstractmethod
    def is_silent(self) -> bool:
        """Get whether the output writes no message."""

    @abstractmethod
    def with_is_silent(self, is_silent: bool) -> Self:
        """Get a copy of the output that records whether it is silent."""

    @abstractmethod
    def get_exit_code(self) -> ExitCode | int:
        """Get the code that the command gives back to the shell."""

    @abstractmethod
    def with_exit_code(self, exit_code: ExitCode | int) -> Self:
        """Get a copy of the output that carries a different exit code."""
