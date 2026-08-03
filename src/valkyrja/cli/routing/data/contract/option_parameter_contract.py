#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self

from valkyrja.cli.interaction.option.contract.option_contract import OptionContract
from valkyrja.cli.routing.data.contract.parameter_contract import ParameterContract
from valkyrja.cli.routing.enum.option_mode import OptionMode
from valkyrja.cli.routing.enum.option_value_mode import OptionValueMode


class OptionParameterContract(ParameterContract):
    """The contract for a named parameter that a command declares."""

    @abstractmethod
    def get_short_names(self) -> list[str]:
        """Get each short name of the option, such as `h` for `-h`."""

    @abstractmethod
    def with_short_names(self, *short_names: str) -> Self:
        """Get a copy of the parameter that carries different short names."""

    @abstractmethod
    def with_added_short_names(self, *short_names: str) -> Self:
        """Get a copy of the parameter that carries more short names."""

    @abstractmethod
    def get_mode(self) -> OptionMode:
        """Get whether the command needs the option."""

    @abstractmethod
    def with_mode(self, mode: OptionMode) -> Self:
        """Get a copy of the parameter that carries a different mode."""

    @abstractmethod
    def get_value_mode(self) -> OptionValueMode:
        """Get whether the option takes no value, one value, or many."""

    @abstractmethod
    def with_value_mode(self, value_mode: OptionValueMode) -> Self:
        """Get a copy of the parameter that carries a different value mode."""

    @abstractmethod
    def has_value_display_name(self) -> bool:
        """Get whether the help text shows a name for the value."""

    @abstractmethod
    def get_value_display_name(self) -> str:
        """Get the name that the help text shows for the value."""

    @abstractmethod
    def with_value_display_name(self, value_name: str) -> Self:
        """Get a copy of the parameter that shows a different name for the value."""

    @abstractmethod
    def get_options(self) -> list[OptionContract]:
        """Get each option that the user gave for this parameter."""

    @abstractmethod
    def with_options(self, *options: OptionContract) -> Self:
        """Get a copy of the parameter that carries different options."""

    @abstractmethod
    def with_added_options(self, *options: OptionContract) -> Self:
        """Get a copy of the parameter that carries more options."""

    @abstractmethod
    def get_valid_values(self) -> list[str]:
        """Get each value that the option accepts."""

    @abstractmethod
    def with_valid_values(self, *valid_values: str) -> Self:
        """Get a copy of the parameter that accepts different values."""

    @abstractmethod
    def with_added_valid_values(self, *valid_values: str) -> Self:
        """Get a copy of the parameter that accepts more values."""
