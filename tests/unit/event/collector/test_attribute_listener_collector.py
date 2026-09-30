#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for AttributeListenerCollector."""

from tests.fixtures.event.collector.listener_class_fixture import (
    ListenerClassFixture,
    UnmarkedClassFixture,
)
from tests.fixtures.event.data.order_event_fixture import ORDER_PLACED_ID, ORDER_SHIPPED_ID
from valkyrja.event.collector.attribute_listener_collector import AttributeListenerCollector


def test_get_listeners_reads_each_marked_function() -> None:
    listeners = AttributeListenerCollector().get_listeners(ListenerClassFixture)

    assert sorted(listener.get_name() for listener in listeners) == [
        "fixture.both.placed",
        "fixture.both.shipped",
        "fixture.order_placed",
    ]


def test_get_listeners_names_the_event_of_each_marker() -> None:
    listeners = AttributeListenerCollector().get_listeners(ListenerClassFixture)
    events = {listener.get_name(): listener.get_event_id() for listener in listeners}

    assert events == {
        "fixture.order_placed": ORDER_PLACED_ID,
        "fixture.both.placed": ORDER_PLACED_ID,
        "fixture.both.shipped": ORDER_SHIPPED_ID,
    }


def test_get_listeners_gives_the_decorated_function_as_the_handler() -> None:
    listeners = AttributeListenerCollector().get_listeners(ListenerClassFixture)
    handlers = {listener.get_name(): listener.get_handler() for listener in listeners}

    assert handlers["fixture.order_placed"] is ListenerClassFixture.on_order_placed
    assert handlers["fixture.both.placed"] is ListenerClassFixture.on_either


def test_get_listeners_keeps_the_order_that_the_decorators_read() -> None:
    listeners = AttributeListenerCollector().get_listeners(ListenerClassFixture)
    both = [listener.get_name() for listener in listeners if listener.get_name().startswith("fixture.both.")]

    assert both == ["fixture.both.placed", "fixture.both.shipped"]


def test_get_listeners_reads_nothing_from_an_unmarked_class() -> None:
    assert AttributeListenerCollector().get_listeners(UnmarkedClassFixture) == []


def test_get_listeners_reads_every_class_it_is_given() -> None:
    listeners = AttributeListenerCollector().get_listeners(ListenerClassFixture, UnmarkedClassFixture)

    assert len(listeners) == 3


def test_get_listeners_with_no_class_is_empty() -> None:
    assert AttributeListenerCollector().get_listeners() == []
