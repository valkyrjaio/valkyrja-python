#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Listener data object."""

from typing import Any

from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.event.data.contract.listener_contract import ListenerContract
from valkyrja.event.data.listener import Listener

EVENT_ID = "tests.unit.event.Event"
NAME = "tests.unit.event.Listener"


def handle(container: ContainerContract, arguments: dict[str, Any]) -> Any:
    return arguments


def other_handle(container: ContainerContract, arguments: dict[str, Any]) -> Any:
    return "other"


def make_listener() -> Listener:
    return Listener(EVENT_ID, NAME, handle)


def test_the_listener_implements_the_contract() -> None:
    assert isinstance(make_listener(), ListenerContract)


def test_get_event_id() -> None:
    assert make_listener().get_event_id() == EVENT_ID


def test_get_name() -> None:
    assert make_listener().get_name() == NAME


def test_get_handler() -> None:
    assert make_listener().get_handler()(Container(), {"key": "value"}) == {"key": "value"}


def test_with_event_id_returns_a_copy() -> None:
    listener = make_listener()

    changed = listener.with_event_id("other")

    assert changed is not listener
    assert changed.get_event_id() == "other"
    assert listener.get_event_id() == EVENT_ID


def test_with_name_returns_a_copy() -> None:
    listener = make_listener()

    changed = listener.with_name("other")

    assert changed is not listener
    assert changed.get_name() == "other"
    assert listener.get_name() == NAME


def test_with_handler_returns_a_copy() -> None:
    listener = make_listener()

    changed = listener.with_handler(other_handle)

    assert changed is not listener
    assert changed.get_handler() is other_handle
    assert listener.get_handler() is handle
