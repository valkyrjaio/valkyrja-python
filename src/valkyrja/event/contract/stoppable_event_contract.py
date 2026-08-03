#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod


class StoppableEventContract(ABC):
    """The contract for an event that can stop the dispatcher part way.

    PHP takes this contract from PSR-14. Python has no PSR, so the framework
    declares it. The dispatcher asks each listener in turn, and it stops as soon
    as the event reports that propagation is stopped.
    """

    @abstractmethod
    def is_propagation_stopped(self) -> bool:
        """Get whether the dispatcher stops before the next listener."""
