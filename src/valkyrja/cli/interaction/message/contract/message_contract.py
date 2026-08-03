#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.cli.interaction.formatter.contract.formatter_contract import FormatterContract


class MessageContract(ABC):
    """The contract for one message that an output writes."""

    @abstractmethod
    def get_text(self) -> str:
        """Get the text of the message."""

    @abstractmethod
    def get_formatted_text(self) -> str:
        """Get the text with the formatter applied to it."""

    @abstractmethod
    def with_text(self, text: str) -> Self:
        """Get a copy of the message that carries a different text."""

    @abstractmethod
    def has_formatter(self) -> bool:
        """Get whether the message carries a formatter."""

    @abstractmethod
    def get_formatter(self) -> FormatterContract:
        """Get the formatter of the message."""

    @abstractmethod
    def with_formatter(self, formatter: FormatterContract) -> Self:
        """Get a copy of the message that carries a different formatter."""

    @abstractmethod
    def without_formatter(self) -> Self:
        """Get a copy of the message that carries no formatter."""
