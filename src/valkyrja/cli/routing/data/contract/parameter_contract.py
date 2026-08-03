#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.type.data.cast import Cast


class ParameterContract(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the parameter."""

    @abstractmethod
    def with_name(self, name: str) -> Self:
        """Get a copy of the parameter that carries a different name."""

    @abstractmethod
    def has_cast(self) -> bool:
        """Get whether the parameter converts its value to a type."""

    @abstractmethod
    def get_cast(self) -> Cast:
        """Get the cast that converts the value of the parameter."""

    @abstractmethod
    def with_cast(self, cast: Cast) -> Self:
        """Get a copy of the parameter that carries a different cast."""

    @abstractmethod
    def without_cast(self) -> Self:
        """Get a copy of the parameter that carries no cast."""

    @abstractmethod
    def get_description(self) -> str:
        """Get the description that the help text shows."""

    @abstractmethod
    def with_description(self, description: str) -> Self:
        """Get a copy of the parameter that carries a different description."""

    @abstractmethod
    def get_values(self) -> list[str]:
        """Get each raw value of the parameter.

        A parameter holds no container, so it applies no cast. `CasterContract` takes
        the cast, because the thing that asks for a cast value does the casting.
        """

    @abstractmethod
    def has_first_value(self) -> bool:
        """Get whether the parameter holds a value."""

    @abstractmethod
    def are_values_valid(self) -> bool:
        """Get whether the values of the parameter are valid."""

    @abstractmethod
    def validate_values(self) -> Self:
        """Get the parameter, and raise when the values are not valid."""
