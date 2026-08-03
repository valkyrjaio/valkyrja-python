#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.cli.interaction.argument.contract.argument_contract import ArgumentContract
from valkyrja.cli.interaction.option.contract.option_contract import OptionContract


class InputContract(ABC):
    """The contract for what the user typed on the command line."""

    @abstractmethod
    def get_caller(self) -> str:
        """Get the name of the program that the user ran."""

    @abstractmethod
    def with_caller(self, caller: str) -> Self:
        """Get a copy of the input that carries a different caller."""

    @abstractmethod
    def get_command_name(self) -> str:
        """Get the name of the command that the user asked for."""

    @abstractmethod
    def with_command_name(self, command_name: str) -> Self:
        """Get a copy of the input that carries a different command name."""

    @abstractmethod
    def get_arguments(self) -> list[ArgumentContract]:
        """Get each positional argument."""

    @abstractmethod
    def with_arguments(self, *arguments: ArgumentContract) -> Self:
        """Get a copy of the input that carries different arguments."""

    @abstractmethod
    def with_added_argument(self, argument: ArgumentContract) -> Self:
        """Get a copy of the input that carries one more argument."""

    @abstractmethod
    def without_argument(self, value: str) -> Self:
        """Get a copy of the input without the argument that has a given value."""

    @abstractmethod
    def without_arguments(self) -> Self:
        """Get a copy of the input that carries no argument."""

    @abstractmethod
    def get_options(self) -> list[OptionContract]:
        """Get each option."""

    @abstractmethod
    def get_option(self, name: str) -> list[OptionContract]:
        """Get each option that carries a given name."""

    @abstractmethod
    def has_option(self, name: str) -> bool:
        """Get whether the input carries an option with a given name."""

    @abstractmethod
    def with_options(self, *options: OptionContract) -> Self:
        """Get a copy of the input that carries different options."""

    @abstractmethod
    def with_added_option(self, option: OptionContract) -> Self:
        """Get a copy of the input that carries one more option."""

    @abstractmethod
    def without_option(self, name: str) -> Self:
        """Get a copy of the input without the option that has a given name."""

    @abstractmethod
    def without_options(self) -> Self:
        """Get a copy of the input that carries no option."""
