#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod

from valkyrja.event.contract.event_contract import EventContract


class StoppableEventContract(EventContract):
    @abstractmethod
    def is_propagation_stopped(self) -> bool:
        """Get whether the dispatcher stops before the next listener."""
