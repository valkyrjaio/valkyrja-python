#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract


class ProgressContract(MessageContract):
    """The contract for a message that reports how far a task has run."""

    @abstractmethod
    def is_complete(self) -> bool:
        """Get whether the task is complete."""

    @abstractmethod
    def with_is_complete(self, is_complete: bool) -> Self:
        """Get a copy of the message that records whether the task is complete."""

    @abstractmethod
    def get_percentage(self) -> int:
        """Get how far the task has run, from 0 to 100."""

    @abstractmethod
    def with_percentage(self, percentage: int) -> Self:
        """Get a copy of the message that carries a different percentage."""
