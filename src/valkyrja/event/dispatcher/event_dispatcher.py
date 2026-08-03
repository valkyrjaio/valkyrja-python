#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, override

from valkyrja.container.enum.invalid_reference_mode import InvalidReferenceMode
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.event.collection.contract.listener_collection_contract import (
    ListenerCollectionContract,
)
from valkyrja.event.constant.event_argument import EVENT_ARGUMENT_KEY
from valkyrja.event.contract.dispatch_collectable_event_contract import (
    DispatchCollectableEventContract,
)
from valkyrja.event.contract.event_contract import EventContract
from valkyrja.event.contract.stoppable_event_contract import StoppableEventContract
from valkyrja.event.data.contract.listener_contract import ListenerContract
from valkyrja.event.dispatcher.contract.event_dispatcher_contract import EventDispatcherContract
from valkyrja.event.throwable.exception.event_invalid_event_exception import (
    EventInvalidEventException,
)


class EventDispatcher(EventDispatcherContract):
    """Runs each listener of an event."""

    def __init__(self, collection: ListenerCollectionContract, container: ContainerContract) -> None:
        self._collection = collection
        self._container = container

    @override
    def dispatch(self, event: EventContract) -> EventContract:
        return self.dispatch_listeners(event, *self._collection.get_listeners_for_event(event))

    @override
    def dispatch_if_has_listeners(self, event: EventContract) -> EventContract:
        if self._collection.has_listeners_for_event(event):
            return self.dispatch(event)

        return event

    @override
    def dispatch_by_id(self, event_id: str, arguments: dict[str, Any] | None = None) -> EventContract:
        return self.dispatch(self._get_event_from_id(event_id, arguments))

    @override
    def dispatch_by_id_if_has_listeners(self, event_id: str, arguments: dict[str, Any] | None = None) -> EventContract:
        event = self._get_event_from_id(event_id, arguments)

        if self._collection.has_listeners_for_event_by_id(event_id):
            return self.dispatch(event)

        return event

    @override
    def dispatch_listeners(self, event: EventContract, *listeners: ListenerContract) -> EventContract:
        for listener in listeners:
            event = self.dispatch_listener(event, listener)

            if isinstance(event, StoppableEventContract) and event.is_propagation_stopped():
                return event

        return event

    @override
    def dispatch_listener(self, event: EventContract, listener: ListenerContract) -> EventContract:
        handler = listener.get_handler()
        dispatch = handler(self._container, {EVENT_ARGUMENT_KEY: event})

        if isinstance(event, DispatchCollectableEventContract):
            event.add_dispatch(dispatch)

        return event

    def _get_event_from_id(self, event_id: str, arguments: dict[str, Any] | None) -> EventContract:
        """Build the event that a binding key names.

        PHP and Java build the event from the class of the event. Python cannot
        construct a type from a string, so this port resolves the binding key
        through the container, which is the answer of the framework to "build
        the thing that this identifier names". Go resolves it the same way. An
        application binds each event that it dispatches by identifier.
        """
        resolved = self._container.get(event_id, arguments, InvalidReferenceMode.NEW_INSTANCE_OR_THROW_EXCEPTION)

        if not isinstance(resolved, EventContract):
            raise EventInvalidEventException(event_id)

        return resolved
