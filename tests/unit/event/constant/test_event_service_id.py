#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for EventServiceId.

Each key is part of the public API, so each test pins the whole string. The key
is the import path that Python has, never the path of another port.
"""

from valkyrja.event.constant.event_service_id import EventServiceId


def test_event_data() -> None:
    assert EventServiceId.EVENT_DATA == "valkyrja.event.data.EventData"


def test_collection_contract() -> None:
    assert EventServiceId.COLLECTION_CONTRACT == "valkyrja.event.collection.ListenerCollectionContract"


def test_collector_contract() -> None:
    assert EventServiceId.COLLECTOR_CONTRACT == "valkyrja.event.collector.ListenerCollectorContract"


def test_dispatcher_contract() -> None:
    assert EventServiceId.DISPATCHER_CONTRACT == "valkyrja.event.dispatcher.EventDispatcherContract"
