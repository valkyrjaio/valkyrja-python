#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod


class EventContract(ABC):
    """A thing that the dispatcher dispatches.

    The event states its own identifier, and that identifier is a container
    binding key. The collection files a listener under it, and the dispatcher
    asks the container for it in `dispatch_by_id`. One identifier therefore
    serves both, which is what lets the dispatcher build an event from a string.

    PHP reads the class of the event instead, and Java holds a `Class<?>`.
    Python could read the class too, but a class name is not a binding key, so
    the two identifiers would not agree. Go states the identifier for the same
    reason.
    """

    @abstractmethod
    def get_event_id(self) -> str:
        """Get the identifier of the event."""
