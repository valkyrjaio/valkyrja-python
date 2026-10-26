#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ListenerContract."""

from typing import Any

import pytest

from tests.fixtures.event.data.listener_fixture import (
    EVENT_ID,
    LISTENER_NAME,
    ListenerFixture,
)
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.event.data.contract.listener_contract import ListenerContract

OTHER_EVENT_ID = "tests.unit.event.OtherEvent"
OTHER_NAME = "tests.unit.event.OtherListener"


def other_handler(container: ContainerContract, arguments: dict[str, Any]) -> Any:
    return "other"


def test_the_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        ListenerContract()  # type: ignore[abstract]


def test_get_event_id() -> None:
    assert ListenerFixture().get_event_id() == EVENT_ID


def test_get_name() -> None:
    assert ListenerFixture().get_name() == LISTENER_NAME


def test_get_handler_returns_the_handler() -> None:
    handler = ListenerFixture().get_handler()

    assert handler(Container(), {"key": "value"}) == {"key": "value"}


def test_with_event_id_returns_a_copy() -> None:
    listener = ListenerFixture()

    changed = listener.with_event_id(OTHER_EVENT_ID)

    assert changed is not listener
    assert changed.get_event_id() == OTHER_EVENT_ID
    assert listener.get_event_id() == EVENT_ID


def test_with_name_returns_a_copy() -> None:
    listener = ListenerFixture()

    changed = listener.with_name(OTHER_NAME)

    assert changed is not listener
    assert changed.get_name() == OTHER_NAME
    assert listener.get_name() == LISTENER_NAME


def test_with_handler_returns_a_copy() -> None:
    listener = ListenerFixture()

    changed = listener.with_handler(other_handler)

    assert changed is not listener
    assert changed.get_handler() is other_handler
    assert listener.get_handler() is not other_handler
