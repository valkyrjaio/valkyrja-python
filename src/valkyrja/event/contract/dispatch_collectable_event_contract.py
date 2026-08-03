#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Any


class DispatchCollectableEventContract(ABC):
    """The contract for an event that keeps what each listener returns."""

    @abstractmethod
    def add_dispatch(self, dispatch: Any) -> None:
        """Add the result of one listener to the event."""

    @abstractmethod
    def get_dispatches(self) -> list[Any]:
        """Get the result of each listener that ran."""
