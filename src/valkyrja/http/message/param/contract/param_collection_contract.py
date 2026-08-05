#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Any, Self


class ParamCollectionContract(ABC):
    """The contract for a collection of parameters that a request carries.

    A value is a scalar, or another collection where the parameters nest.
    """

    @abstractmethod
    def has(self, key: str | int) -> bool:
        """Get whether the collection holds a parameter under a given key."""

    @abstractmethod
    def get(self, key: str | int) -> Any:
        """Get the parameter under a given key, or `None` when it holds none."""

    @abstractmethod
    def get_all(self) -> dict[str | int, Any]:
        """Get every parameter."""

    @abstractmethod
    def get_only(self, *keys: str | int) -> dict[str | int, Any]:
        """Get the parameter for each key that the caller names."""

    @abstractmethod
    def get_all_except(self, *keys: str | int) -> dict[str | int, Any]:
        """Get every parameter except the ones that the caller names."""

    @abstractmethod
    def with_(self, params: dict[str | int, Any]) -> Self:
        """Get a copy of the collection that holds different parameters.

        The name ends in an underscore, because `with` is a reserved word.
        """

    @abstractmethod
    def with_added(self, params: dict[str | int, Any]) -> Self:
        """Get a copy of the collection that holds more parameters."""
