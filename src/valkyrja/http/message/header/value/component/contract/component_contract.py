#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self


class ComponentContract(ABC):
    """The contract for one part of a header value, such as `charset=utf-8`."""

    @abstractmethod
    def __str__(self) -> str:
        """Get the component as a string."""

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the component."""

    @abstractmethod
    def with_name(self, name: str) -> Self:
        """Get a copy of the component that carries a different name."""

    @abstractmethod
    def get_value(self) -> str:
        """Get the value of the component."""

    @abstractmethod
    def with_value(self, value: str) -> Self:
        """Get a copy of the component that carries a different value."""
