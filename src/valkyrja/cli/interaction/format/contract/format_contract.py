#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self


class FormatContract(ABC):
    """The contract for one ANSI format, which has a code to set and a code to unset."""

    @abstractmethod
    def get_set_code(self) -> str:
        """Get the code that starts the format."""

    @abstractmethod
    def with_set_code(self, set_code: str) -> Self:
        """Get a copy of the format that starts with a different code."""

    @abstractmethod
    def get_unset_code(self) -> str:
        """Get the code that ends the format."""

    @abstractmethod
    def with_unset_code(self, unset_code: str) -> Self:
        """Get a copy of the format that ends with a different code."""
