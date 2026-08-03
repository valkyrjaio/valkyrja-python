#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self

from valkyrja.cli.interaction.argument.contract.argument_contract import ArgumentContract
from valkyrja.cli.routing.data.contract.parameter_contract import ParameterContract
from valkyrja.cli.routing.enum.argument_mode import ArgumentMode
from valkyrja.cli.routing.enum.argument_value_mode import ArgumentValueMode


class ArgumentParameterContract(ParameterContract):
    """The contract for a positional parameter that a command declares."""

    @abstractmethod
    def get_mode(self) -> ArgumentMode:
        """Get whether the command needs the argument."""

    @abstractmethod
    def with_mode(self, mode: ArgumentMode) -> Self:
        """Get a copy of the parameter that carries a different mode."""

    @abstractmethod
    def get_value_mode(self) -> ArgumentValueMode:
        """Get whether the argument takes one value or many."""

    @abstractmethod
    def with_value_mode(self, value_mode: ArgumentValueMode) -> Self:
        """Get a copy of the parameter that carries a different value mode."""

    @abstractmethod
    def get_arguments(self) -> list[ArgumentContract]:
        """Get each argument that the user gave for this parameter."""

    @abstractmethod
    def with_arguments(self, *arguments: ArgumentContract) -> Self:
        """Get a copy of the parameter that carries different arguments."""

    @abstractmethod
    def with_added_arguments(self, *arguments: ArgumentContract) -> Self:
        """Get a copy of the parameter that carries more arguments."""
