#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from collections.abc import Callable
from dataclasses import dataclass, field

from valkyrja.event.data.contract.listener_contract import ListenerContract

type ListenerFactory = Callable[[], ListenerContract]
"""The collection calls this factory to build a listener that the cache holds."""


@dataclass(frozen=True)
class EventData:
    """A data representation of the state of a listener collection.

    `events` maps an event id to the name of each listener for that event.
    `listeners` maps a listener name to the factory that builds the listener.
    """

    events: dict[str, list[str]] = field(default_factory=dict)
    listeners: dict[str, ListenerFactory] = field(default_factory=dict)
