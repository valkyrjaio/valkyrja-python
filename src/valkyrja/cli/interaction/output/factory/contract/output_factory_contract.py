#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.output.contract.empty_output_contract import EmptyOutputContract
from valkyrja.cli.interaction.output.contract.file_output_contract import FileOutputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.contract.plain_output_contract import PlainOutputContract
from valkyrja.cli.interaction.output.contract.stream_output_contract import StreamOutputContract


class OutputFactoryContract(ABC):
    """The contract for the factory that builds each kind of output."""

    @abstractmethod
    def create_output(self, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract) -> OutputContract:
        """Build the default output."""

    @abstractmethod
    def create_empty_output(
        self, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract
    ) -> EmptyOutputContract:
        """Build an output that writes nothing."""

    @abstractmethod
    def create_plain_output(
        self, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract
    ) -> PlainOutputContract:
        """Build an output that writes no ANSI format."""

    @abstractmethod
    def create_file_output(
        self, filepath: str, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract
    ) -> FileOutputContract:
        """Build an output that writes to a file."""

    @abstractmethod
    def create_stream_output(
        self, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract
    ) -> StreamOutputContract:
        """Build an output that writes to a stream."""
