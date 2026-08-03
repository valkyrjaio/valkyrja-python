#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.event.collection.contract.listener_collection_contract import (
    ListenerCollectionContract,
)
from valkyrja.event.data.contract.listener_contract import ListenerContract
from valkyrja.event.data.event_data import EventData, ListenerFactory
from valkyrja.support.factory.class_name_factory import ClassNameFactory


class ListenerCollection(ListenerCollectionContract):
    """Holds each listener, and holds the listeners of each event.

    The collection stores a factory for each listener, never the listener
    itself. `sindri` writes a factory into the generated cache, so the runtime
    map and the cache hold the same shape.
    """

    def __init__(self) -> None:
        self._events: dict[str, list[str]] = {}
        self._listeners: dict[str, ListenerFactory] = {}

    @override
    def get_data(self) -> EventData:
        return EventData(
            events={event_id: list(names) for event_id, names in self._events.items()},
            listeners=dict(self._listeners),
        )

    @override
    def set_from_data(self, data: EventData) -> None:
        self._events = {event_id: list(names) for event_id, names in data.events.items()}
        self._listeners = dict(data.listeners)

    @override
    def has_listener(self, listener: ListenerContract) -> bool:
        return self.has_listener_by_id(listener.get_name())

    @override
    def has_listener_by_id(self, listener_id: str) -> bool:
        return listener_id in self._listeners

    @override
    def add_listener(self, listener: ListenerContract) -> None:
        listener_id = listener.get_name()
        event_id = listener.get_event_id()
        names = self._events.setdefault(event_id, [])

        if listener_id not in names:
            names.append(listener_id)

        self._listeners[listener_id] = lambda: listener

    @override
    def remove_listener(self, listener: ListenerContract) -> None:
        listener_id = listener.get_name()
        event_id = listener.get_event_id()
        names = self._events.get(event_id)

        if names is not None and listener_id in names:
            names.remove(listener_id)

        self._listeners.pop(listener_id, None)

    @override
    def remove_listener_by_id(self, listener_id: str) -> None:
        for names in self._events.values():
            if listener_id in names:
                names.remove(listener_id)

        self._listeners.pop(listener_id, None)

    @override
    def has_listeners_for_event(self, event: object) -> bool:
        return self.has_listeners_for_event_by_id(ClassNameFactory.class_of(event))

    @override
    def has_listeners_for_event_by_id(self, event_id: str) -> bool:
        return bool(self._events.get(event_id))

    @override
    def get_listeners_for_event(self, event: object) -> list[ListenerContract]:
        return self.get_listeners_for_event_by_id(ClassNameFactory.class_of(event))

    @override
    def get_listeners_for_event_by_id(self, event_id: str) -> list[ListenerContract]:
        names = self._events.get(event_id)

        if names is None:
            return []

        return [self._listeners[name]() for name in names]

    @override
    def set_listeners_for_event(self, event: object, *listeners: ListenerContract) -> None:
        self.set_listeners_for_event_by_id(ClassNameFactory.class_of(event), *listeners)

    @override
    def set_listeners_for_event_by_id(self, event_id: str, *listeners: ListenerContract) -> None:
        for listener in listeners:
            self.add_listener(listener.with_event_id(event_id))

    @override
    def remove_listeners_for_event(self, event: object) -> None:
        self.remove_listeners_for_event_by_id(ClassNameFactory.class_of(event))

    @override
    def remove_listeners_for_event_by_id(self, event_id: str) -> None:
        for listener in self.get_listeners_for_event_by_id(event_id):
            self.remove_listener(listener)

        self._events.pop(event_id, None)

    @override
    def get_listeners(self) -> list[ListenerContract]:
        return [factory() for factory in self._listeners.values()]

    @override
    def get_events(self) -> list[str]:
        return list(self._events)

    @override
    def get_events_with_listeners(self) -> dict[str, list[ListenerContract]]:
        return {event_id: self.get_listeners_for_event_by_id(event_id) for event_id in self._events}
