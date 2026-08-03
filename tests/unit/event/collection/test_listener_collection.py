#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ListenerCollection."""

from typing import Any

from tests.fixtures.event.data.order_event_fixture import (
    ORDER_PLACED_ID,
    ORDER_SHIPPED_ID,
    OrderPlacedFixture,
    OrderShippedFixture,
)
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.event.collection.listener_collection import ListenerCollection
from valkyrja.event.data.event_data import EventData
from valkyrja.event.data.listener import Listener


def handle(container: ContainerContract, arguments: dict[str, Any]) -> Any:
    return arguments


def make_listener(name: str = "first", event_id: str = ORDER_PLACED_ID) -> Listener:
    return Listener(event_id, name, handle)


def test_a_new_collection_is_empty() -> None:
    collection = ListenerCollection()

    assert collection.get_listeners() == []
    assert collection.get_events() == []
    assert collection.get_events_with_listeners() == {}


def test_add_listener_registers_the_listener_and_the_event() -> None:
    collection = ListenerCollection()
    listener = make_listener()

    collection.add_listener(listener)

    assert collection.has_listener(listener)
    assert collection.has_listener_by_id("first")
    assert collection.get_events() == [ORDER_PLACED_ID]


def test_add_listener_twice_registers_the_name_once() -> None:
    collection = ListenerCollection()

    collection.add_listener(make_listener())
    collection.add_listener(make_listener())

    assert collection.get_listeners_for_event_by_id(ORDER_PLACED_ID) == [
        collection.get_listeners_for_event_by_id(ORDER_PLACED_ID)[0]
    ]
    assert len(collection.get_listeners_for_event_by_id(ORDER_PLACED_ID)) == 1


def test_has_listener_is_false_for_an_unknown_listener() -> None:
    assert not ListenerCollection().has_listener(make_listener())
    assert not ListenerCollection().has_listener_by_id("missing")


def test_get_listeners_for_event_reads_the_class_of_the_event() -> None:
    collection = ListenerCollection()
    collection.add_listener(make_listener())

    listeners = collection.get_listeners_for_event(OrderPlacedFixture())

    assert [listener.get_name() for listener in listeners] == ["first"]


def test_get_listeners_for_an_event_with_none_is_empty() -> None:
    assert ListenerCollection().get_listeners_for_event_by_id(ORDER_SHIPPED_ID) == []


def test_has_listeners_for_event() -> None:
    collection = ListenerCollection()

    assert not collection.has_listeners_for_event(OrderPlacedFixture())

    collection.add_listener(make_listener())

    assert collection.has_listeners_for_event(OrderPlacedFixture())
    assert not collection.has_listeners_for_event(OrderShippedFixture())


def test_has_listeners_for_event_is_false_once_the_last_listener_goes() -> None:
    collection = ListenerCollection()
    listener = make_listener()
    collection.add_listener(listener)

    collection.remove_listener(listener)

    assert not collection.has_listeners_for_event_by_id(ORDER_PLACED_ID)


def test_remove_listener_drops_the_listener() -> None:
    collection = ListenerCollection()
    listener = make_listener()
    collection.add_listener(listener)

    collection.remove_listener(listener)

    assert not collection.has_listener(listener)
    assert collection.get_listeners() == []


def test_remove_listener_accepts_a_listener_the_collection_never_held() -> None:
    collection = ListenerCollection()

    collection.remove_listener(make_listener())

    assert collection.get_listeners() == []


def test_remove_listener_by_id_drops_it_from_every_event() -> None:
    collection = ListenerCollection()
    collection.add_listener(make_listener("shared", ORDER_PLACED_ID))
    collection.set_listeners_for_event_by_id(ORDER_SHIPPED_ID, make_listener("shared", ORDER_PLACED_ID))

    collection.remove_listener_by_id("shared")

    assert not collection.has_listener_by_id("shared")
    assert collection.get_listeners_for_event_by_id(ORDER_PLACED_ID) == []
    assert collection.get_listeners_for_event_by_id(ORDER_SHIPPED_ID) == []


def test_remove_listener_by_id_accepts_an_unknown_id() -> None:
    collection = ListenerCollection()
    collection.add_listener(make_listener())

    collection.remove_listener_by_id("missing")

    assert collection.has_listener_by_id("first")


def test_set_listeners_for_event_moves_each_listener_to_that_event() -> None:
    collection = ListenerCollection()

    collection.set_listeners_for_event(OrderShippedFixture(), make_listener("first"))

    assert collection.get_listeners_for_event_by_id(ORDER_SHIPPED_ID)[0].get_event_id() == ORDER_SHIPPED_ID


def test_remove_listeners_for_event_drops_the_event() -> None:
    collection = ListenerCollection()
    collection.add_listener(make_listener())

    collection.remove_listeners_for_event(OrderPlacedFixture())

    assert collection.get_events() == []
    assert collection.get_listeners() == []


def test_remove_listeners_for_an_event_with_none_is_safe() -> None:
    collection = ListenerCollection()

    collection.remove_listeners_for_event_by_id(ORDER_SHIPPED_ID)

    assert collection.get_events() == []


def test_get_events_with_listeners() -> None:
    collection = ListenerCollection()
    collection.add_listener(make_listener())

    events = collection.get_events_with_listeners()

    assert list(events) == [ORDER_PLACED_ID]
    assert [listener.get_name() for listener in events[ORDER_PLACED_ID]] == ["first"]


def test_get_data_returns_the_state() -> None:
    collection = ListenerCollection()
    collection.add_listener(make_listener())

    data = collection.get_data()

    assert data.events == {ORDER_PLACED_ID: ["first"]}
    assert data.listeners["first"]().get_name() == "first"


def test_get_data_copies_the_state() -> None:
    collection = ListenerCollection()
    collection.add_listener(make_listener())

    collection.get_data().events[ORDER_PLACED_ID].clear()

    assert collection.get_listeners_for_event_by_id(ORDER_PLACED_ID) != []


def test_set_from_data_replaces_the_state() -> None:
    collection = ListenerCollection()
    listener = make_listener("cached")

    collection.set_from_data(EventData(events={ORDER_PLACED_ID: ["cached"]}, listeners={"cached": lambda: listener}))

    assert collection.has_listener_by_id("cached")
    assert collection.get_listeners_for_event_by_id(ORDER_PLACED_ID) == [listener]


def test_set_from_data_copies_the_state() -> None:
    collection = ListenerCollection()
    data = EventData(events={ORDER_PLACED_ID: ["cached"]}, listeners={"cached": make_listener})

    collection.set_from_data(data)
    data.events[ORDER_PLACED_ID].clear()

    assert collection.get_listeners_for_event_by_id(ORDER_PLACED_ID) != []
