#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.event.data.contract.listener_contract import ListenerContract
from valkyrja.event.data.event_data import EventData


class ListenerCollectionContract(ABC):
    """The contract for the collection that holds each listener.

    PHP extends the PSR-14 `ListenerProviderInterface`. Python has no PSR, so
    this contract declares `get_listeners_for_event` itself.
    """

    @abstractmethod
    def get_data(self) -> EventData:
        """Get a data representation of the collection."""

    @abstractmethod
    def set_from_data(self, data: EventData) -> None:
        """Add the state of a data object to the collection."""

    @abstractmethod
    def has_listener(self, listener: ListenerContract) -> bool:
        """Get whether the collection holds a given listener."""

    @abstractmethod
    def has_listener_by_id(self, listener_id: str) -> bool:
        """Get whether the collection holds a listener with a given name."""

    @abstractmethod
    def add_listener(self, listener: ListenerContract) -> None:
        """Add a listener to the collection."""

    @abstractmethod
    def remove_listener(self, listener: ListenerContract) -> None:
        """Remove a listener from the collection."""

    @abstractmethod
    def remove_listener_by_id(self, listener_id: str) -> None:
        """Remove the listener with a given name from the collection."""

    @abstractmethod
    def has_listeners_for_event(self, event: object) -> bool:
        """Get whether the collection holds a listener for a given event."""

    @abstractmethod
    def has_listeners_for_event_by_id(self, event_id: str) -> bool:
        """Get whether the collection holds a listener for a given event id."""

    @abstractmethod
    def get_listeners_for_event(self, event: object) -> list[ListenerContract]:
        """Get each listener for a given event."""

    @abstractmethod
    def get_listeners_for_event_by_id(self, event_id: str) -> list[ListenerContract]:
        """Get each listener for a given event id."""

    @abstractmethod
    def set_listeners_for_event(self, event: object, *listeners: ListenerContract) -> None:
        """Set the listeners for a given event, and drop the listeners it had."""

    @abstractmethod
    def set_listeners_for_event_by_id(self, event_id: str, *listeners: ListenerContract) -> None:
        """Set the listeners for a given event id, and drop the listeners it had."""

    @abstractmethod
    def remove_listeners_for_event(self, event: object) -> None:
        """Remove each listener for a given event."""

    @abstractmethod
    def remove_listeners_for_event_by_id(self, event_id: str) -> None:
        """Remove each listener for a given event id."""

    @abstractmethod
    def get_listeners(self) -> list[ListenerContract]:
        """Get each listener that the collection holds."""

    @abstractmethod
    def get_events(self) -> list[str]:
        """Get the id of each event that has a listener."""

    @abstractmethod
    def get_events_with_listeners(self) -> dict[str, list[ListenerContract]]:
        """Get each event id, with the listeners of that event."""
