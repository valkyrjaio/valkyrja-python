#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract

if TYPE_CHECKING:
    from valkyrja.cli.interaction.output.contract.output_contract import OutputContract


class WriterContract(ABC):
    """The contract for the writer that puts one message on an output.

    The import of `OutputContract` is for the type checker alone. An output
    holds a writer, so a plain import would make the two modules import each
    other.
    """

    @abstractmethod
    def should_write_message(self, message: MessageContract) -> bool:
        """Get whether this writer writes a given message."""

    @abstractmethod
    def write(self, output: OutputContract, message: MessageContract) -> OutputContract:
        """Write a message, and get the output back."""
