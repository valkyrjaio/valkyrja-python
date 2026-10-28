#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import cast, final, override

from valkyrja.event.attribute.listener import LISTENER_MARKER, ListenerMarker
from valkyrja.event.collector.contract.listener_collector_contract import (
    ListenerCollectorContract,
)
from valkyrja.event.data.contract.listener_contract import ListenerContract, ListenerHandler
from valkyrja.event.data.listener import Listener


@final
class AttributeListenerCollector(ListenerCollectorContract):
    @override
    def get_listeners(self, *classes: type) -> list[ListenerContract]:
        listeners: list[ListenerContract] = []

        for listener_class in classes:
            listeners.extend(self._get_listeners_for_class(listener_class))

        return listeners

    def _get_listeners_for_class(self, listener_class: type) -> list[ListenerContract]:
        """Read each marked function of one class."""
        listeners: list[ListenerContract] = []

        for member in self._get_marked_members(listener_class):
            markers: tuple[ListenerMarker, ...] = getattr(member, LISTENER_MARKER, ())
            listeners.extend(self._make_listener(marker, member) for marker in markers)

        return listeners

    @staticmethod
    def _get_marked_members(listener_class: type) -> list[ListenerHandler]:
        """Read each marked function the class declares, in declaration order."""
        members: list[ListenerHandler] = []
        seen: set[str] = set()

        # `vars` keeps declaration order, where `inspect.getmembers` sorts by name, and
        # dispatch runs a listener in the order the collector reads it.
        for klass in listener_class.__mro__:
            for name, value in vars(klass).items():
                if name in seen:
                    continue

                function = AttributeListenerCollector._get_function(value, listener_class)

                if callable(function) and hasattr(function, LISTENER_MARKER):
                    seen.add(name)
                    # The marker is what declares the signature, and `vars` types a
                    # member as `Any`, so the cast carries what the marker guarantees.
                    members.append(cast(ListenerHandler, function))

        return members

    @staticmethod
    def _get_function(value: object, listener_class: type) -> object:
        """Get the callable a member holds, in the form that dispatch calls.

        A `classmethod` binds to the class, because dispatch gives the handler the
        container first and the raw function would take that container as `cls`. A
        `staticmethod` holds a plain function, which takes the container already.
        """
        if isinstance(value, classmethod):
            return value.__get__(None, listener_class)

        if isinstance(value, staticmethod):
            return value.__func__

        return value

    @staticmethod
    def _make_listener(marker: ListenerMarker, handler: ListenerHandler) -> ListenerContract:
        """Build a listener from the marker and the function that answers it."""
        return Listener(event_id=marker.event_id, name=marker.name, handler=handler)
