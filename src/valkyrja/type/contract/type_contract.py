#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Self


class TypeContract(ABC):
    """The contract for a value that the framework converts between forms."""

    @abstractmethod
    def as_value(self) -> Any:
        """Get the value in its own form."""

    @abstractmethod
    def as_flat_value(self) -> str | int | float | bool | None:
        """Get the value in a form that a string, a number, or a boolean holds."""

    @abstractmethod
    def modify(self, closure: Callable[[Any], Any]) -> Self:
        """Get a copy of the type, with the closure applied to the value."""
