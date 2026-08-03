#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Any

from valkyrja.event.contract.event_contract import EventContract
from valkyrja.event.data.contract.listener_contract import ListenerContract


class EventDispatcherContract(ABC):
    """The contract for the dispatcher that fires an event to each listener.

    PHP extends the PSR-14 `EventDispatcherInterface`. Python has no PSR, so
    this contract declares `dispatch` itself.
    """

    @abstractmethod
    def dispatch(self, event: EventContract) -> EventContract:
        """Fire an event to each listener, and get the event back."""

    @abstractmethod
    def dispatch_if_has_listeners(self, event: EventContract) -> EventContract:
        """Fire an event only when the event has a listener."""

    @abstractmethod
    def dispatch_by_id(self, event_id: str, arguments: dict[str, Any] | None = None) -> EventContract:
        """Build an event from an id and the arguments, then fire the event."""

    @abstractmethod
    def dispatch_by_id_if_has_listeners(self, event_id: str, arguments: dict[str, Any] | None = None) -> EventContract:
        """Build an event from an id and fire it, only when the event has a listener."""

    @abstractmethod
    def dispatch_listeners(self, event: EventContract, *listeners: ListenerContract) -> EventContract:
        """Fire an event to each listener that the caller gives."""

    @abstractmethod
    def dispatch_listener(self, event: EventContract, listener: ListenerContract) -> EventContract:
        """Fire an event to one listener."""
