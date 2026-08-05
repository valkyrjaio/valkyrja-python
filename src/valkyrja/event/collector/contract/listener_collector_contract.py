#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.event.data.contract.listener_contract import ListenerContract


class ListenerCollectorContract(ABC):
    """The contract for the collector that reads a listener from a class."""

    @abstractmethod
    def get_listeners(self, *classes: type) -> list[ListenerContract]:
        """Get each listener that the given classes declare."""
