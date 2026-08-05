#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.cli.interaction.enum.option_type import OptionType


class OptionContract(ABC):
    """The contract for one named option of a command, such as `--help`."""

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the option, without the dashes."""

    @abstractmethod
    def with_name(self, name: str) -> Self:
        """Get a copy of the option that carries a different name."""

    @abstractmethod
    def has_value(self) -> bool:
        """Get whether the option carries a value."""

    @abstractmethod
    def get_value(self) -> str:
        """Get the value of the option."""

    @abstractmethod
    def with_value(self, value: str) -> Self:
        """Get a copy of the option that carries a different value."""

    @abstractmethod
    def without_value(self) -> Self:
        """Get a copy of the option that carries no value."""

    @abstractmethod
    def get_type(self) -> OptionType:
        """Get the form that the option takes on the command line."""

    @abstractmethod
    def with_type(self, type_: OptionType) -> Self:
        """Get a copy of the option that takes a different form."""
