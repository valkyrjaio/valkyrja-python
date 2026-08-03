#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self


class ArgumentContract(ABC):
    """The contract for one positional argument of a command."""

    @abstractmethod
    def get_value(self) -> str:
        """Get the value of the argument."""

    @abstractmethod
    def with_value(self, value: str) -> Self:
        """Get a copy of the argument that carries a different value."""
