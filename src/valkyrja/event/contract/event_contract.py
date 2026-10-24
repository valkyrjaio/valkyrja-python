#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod


class EventContract(ABC):
    @abstractmethod
    def get_event_id(self) -> str:
        """Get the identifier of the event."""
