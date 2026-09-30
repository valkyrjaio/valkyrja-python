#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import inspect
from typing import override

from valkyrja.event.attribute.listener import LISTENER_MARKER, ListenerMarker
from valkyrja.event.collector.contract.listener_collector_contract import (
    ListenerCollectorContract,
)
from valkyrja.event.data.contract.listener_contract import ListenerContract, ListenerHandler
from valkyrja.event.data.listener import Listener


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

        for _name, member in inspect.getmembers(listener_class, inspect.isfunction):
            markers: tuple[ListenerMarker, ...] = getattr(member, LISTENER_MARKER, ())
            listeners.extend(self._make_listener(marker, member) for marker in markers)

        return listeners

    @staticmethod
    def _make_listener(marker: ListenerMarker, handler: ListenerHandler) -> ListenerContract:
        """Build a listener from the marker and the function that answers it."""
        return Listener(event_id=marker.event_id, name=marker.name, handler=handler)
