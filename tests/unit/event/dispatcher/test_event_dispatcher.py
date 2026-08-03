#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the EventDispatcher."""

from typing import Any

import pytest

from tests.fixtures.event.data.event_fixture import EVENT_ID, EventFixture
from tests.fixtures.event.data.order_event_fixture import ORDER_PLACED_ID, OrderPlacedFixture
from tests.fixtures.event.data.stoppable_event_fixture import (
    STOPPABLE_EVENT_ID,
    StoppableEventFixture,
)
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.event.collection.listener_collection import ListenerCollection
from valkyrja.event.constant.event_argument import EVENT_ARGUMENT_KEY
from valkyrja.event.data.listener import Listener
from valkyrja.event.dispatcher.event_dispatcher import EventDispatcher
from valkyrja.event.throwable.exception.event_invalid_event_exception import (
    EventInvalidEventException,
)

NOT_AN_EVENT_ID = "Valkyrja.Tests.NotAnEvent"
MISSING_ID = "Valkyrja.Tests.Missing"


def make_dispatcher(container: ContainerContract | None = None) -> tuple[EventDispatcher, ListenerCollection]:
    collection = ListenerCollection()

    return EventDispatcher(collection, container if container is not None else Container()), collection


def record_handler(name: str, calls: list[str]) -> Any:
    def handler(container: ContainerContract, arguments: dict[str, Any]) -> Any:
        calls.append(name)

        return name

    return handler


def test_dispatch_runs_each_listener_in_order() -> None:
    calls: list[str] = []
    dispatcher, collection = make_dispatcher()
    collection.add_listener(Listener(ORDER_PLACED_ID, "first", record_handler("first", calls)))
    collection.add_listener(Listener(ORDER_PLACED_ID, "second", record_handler("second", calls)))

    event = OrderPlacedFixture()

    assert dispatcher.dispatch(event) is event
    assert calls == ["first", "second"]


def test_dispatch_passes_the_event_in_the_arguments() -> None:
    seen: list[Any] = []

    def handler(container: ContainerContract, arguments: dict[str, Any]) -> Any:
        seen.append(arguments[EVENT_ARGUMENT_KEY])

        return None

    dispatcher, collection = make_dispatcher()
    collection.add_listener(Listener(ORDER_PLACED_ID, "first", handler))
    event = OrderPlacedFixture()

    dispatcher.dispatch(event)

    assert seen == [event]


def test_dispatch_passes_the_container_to_the_handler() -> None:
    container = Container()
    seen: list[Any] = []

    def handler(passed: ContainerContract, arguments: dict[str, Any]) -> Any:
        seen.append(passed)

        return None

    dispatcher, collection = make_dispatcher(container)
    collection.add_listener(Listener(ORDER_PLACED_ID, "first", handler))

    dispatcher.dispatch(OrderPlacedFixture())

    assert seen == [container]


def test_dispatch_with_no_listener_returns_the_event() -> None:
    dispatcher, _ = make_dispatcher()
    event = OrderPlacedFixture()

    assert dispatcher.dispatch(event) is event


def test_a_collectable_event_keeps_what_each_listener_returned() -> None:
    calls: list[str] = []
    dispatcher, collection = make_dispatcher()
    collection.add_listener(Listener(EVENT_ID, "first", record_handler("first", calls)))
    collection.add_listener(Listener(EVENT_ID, "second", record_handler("second", calls)))

    event = EventFixture()
    dispatcher.dispatch(event)

    assert event.get_dispatches() == ["first", "second"]


def test_a_stoppable_event_stops_the_listeners_after_it() -> None:
    calls: list[str] = []

    def stopping_handler(container: ContainerContract, arguments: dict[str, Any]) -> Any:
        calls.append("first")
        event = arguments[EVENT_ARGUMENT_KEY]
        event.stop()

        return None

    dispatcher, collection = make_dispatcher()
    collection.add_listener(Listener(STOPPABLE_EVENT_ID, "first", stopping_handler))
    collection.add_listener(Listener(STOPPABLE_EVENT_ID, "second", record_handler("second", calls)))

    dispatcher.dispatch(StoppableEventFixture())

    assert calls == ["first"]


def test_a_stoppable_event_that_does_not_stop_runs_every_listener() -> None:
    calls: list[str] = []
    dispatcher, collection = make_dispatcher()
    collection.add_listener(Listener(STOPPABLE_EVENT_ID, "first", record_handler("first", calls)))
    collection.add_listener(Listener(STOPPABLE_EVENT_ID, "second", record_handler("second", calls)))

    dispatcher.dispatch(StoppableEventFixture())

    assert calls == ["first", "second"]


def test_dispatch_if_has_listeners_runs_them() -> None:
    calls: list[str] = []
    dispatcher, collection = make_dispatcher()
    collection.add_listener(Listener(ORDER_PLACED_ID, "first", record_handler("first", calls)))

    dispatcher.dispatch_if_has_listeners(OrderPlacedFixture())

    assert calls == ["first"]


def test_dispatch_if_has_listeners_does_nothing_without_one() -> None:
    calls: list[str] = []
    dispatcher, _ = make_dispatcher()
    event = OrderPlacedFixture()

    assert dispatcher.dispatch_if_has_listeners(event) is event
    assert calls == []


def test_dispatch_by_id_builds_the_event_from_the_container() -> None:
    container = Container()
    container.bind(ORDER_PLACED_ID, lambda c, a: OrderPlacedFixture())
    calls: list[str] = []
    dispatcher, collection = make_dispatcher(container)
    collection.add_listener(Listener(ORDER_PLACED_ID, "first", record_handler("first", calls)))

    dispatched = dispatcher.dispatch_by_id(ORDER_PLACED_ID)

    assert isinstance(dispatched, OrderPlacedFixture)
    assert calls == ["first"]


def test_dispatch_by_id_passes_the_arguments_to_the_container() -> None:
    seen: list[Any] = []
    container = Container()

    def build(passed: ContainerContract, arguments: dict[str, Any]) -> object:
        seen.append(arguments)

        return OrderPlacedFixture()

    container.bind(ORDER_PLACED_ID, build)
    dispatcher, _ = make_dispatcher(container)

    dispatcher.dispatch_by_id(ORDER_PLACED_ID, {"key": "value"})

    assert seen == [{"key": "value"}]


def test_dispatch_by_id_raises_when_the_id_is_not_an_event() -> None:
    container = Container()
    container.bind(NOT_AN_EVENT_ID, lambda c, a: {"not": "an event"})
    dispatcher, _ = make_dispatcher(container)

    with pytest.raises(EventInvalidEventException, match="is not an event"):
        dispatcher.dispatch_by_id(NOT_AN_EVENT_ID)


def test_dispatch_by_id_raises_when_the_container_has_no_binding() -> None:
    dispatcher, _ = make_dispatcher()

    with pytest.raises(Exception, match="not found"):
        dispatcher.dispatch_by_id(MISSING_ID)


def test_dispatch_by_id_if_has_listeners_runs_them() -> None:
    container = Container()
    container.bind(ORDER_PLACED_ID, lambda c, a: OrderPlacedFixture())
    calls: list[str] = []
    dispatcher, collection = make_dispatcher(container)
    collection.add_listener(Listener(ORDER_PLACED_ID, "first", record_handler("first", calls)))

    dispatcher.dispatch_by_id_if_has_listeners(ORDER_PLACED_ID)

    assert calls == ["first"]


def test_dispatch_by_id_if_has_listeners_builds_the_event_without_one() -> None:
    container = Container()
    container.bind(ORDER_PLACED_ID, lambda c, a: OrderPlacedFixture())
    dispatcher, _ = make_dispatcher(container)

    dispatched = dispatcher.dispatch_by_id_if_has_listeners(ORDER_PLACED_ID)

    assert isinstance(dispatched, OrderPlacedFixture)


def test_dispatch_listener_returns_the_event() -> None:
    calls: list[str] = []
    dispatcher, _ = make_dispatcher()
    event = OrderPlacedFixture()
    listener = Listener(ORDER_PLACED_ID, "first", record_handler("first", calls))

    assert dispatcher.dispatch_listener(event, listener) is event
    assert calls == ["first"]


def test_dispatch_listeners_with_none_returns_the_event() -> None:
    dispatcher, _ = make_dispatcher()
    event = OrderPlacedFixture()

    assert dispatcher.dispatch_listeners(event) is event
