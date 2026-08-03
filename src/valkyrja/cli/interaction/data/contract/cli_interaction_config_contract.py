#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod


class CliInteractionConfigContract(ABC):
    """The contract for the configuration of the Cli Interaction subcomponent.

    PHP declares each setting as a property with a getter and a setter. Python
    spells the same shape with a property that has a setter.
    """

    @property
    @abstractmethod
    def is_quiet(self) -> bool:
        """Get whether the output writes a message of low importance."""

    @is_quiet.setter
    @abstractmethod
    def is_quiet(self, is_quiet: bool) -> None:
        """Set whether the output writes a message of low importance."""

    @property
    @abstractmethod
    def is_interactive(self) -> bool:
        """Get whether the output asks a question of the user."""

    @is_interactive.setter
    @abstractmethod
    def is_interactive(self, is_interactive: bool) -> None:
        """Set whether the output asks a question of the user."""

    @property
    @abstractmethod
    def is_silent(self) -> bool:
        """Get whether the output writes no message."""

    @is_silent.setter
    @abstractmethod
    def is_silent(self, is_silent: bool) -> None:
        """Set whether the output writes no message."""
