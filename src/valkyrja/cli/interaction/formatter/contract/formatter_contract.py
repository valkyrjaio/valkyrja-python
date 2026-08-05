#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.cli.interaction.format.contract.format_contract import FormatContract


class FormatterContract(ABC):
    """The contract for the formatter that puts each format around a text."""

    @abstractmethod
    def get_formats(self) -> list[FormatContract]:
        """Get each format that the formatter applies."""

    @abstractmethod
    def with_formats(self, *formats: FormatContract) -> Self:
        """Get a copy of the formatter that applies different formats."""

    @abstractmethod
    def format_text(self, text: str) -> str:
        """Get the text with each format around it."""
