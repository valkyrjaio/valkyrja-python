#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for EventData."""

import dataclasses

import pytest

from tests.fixtures.event.data.listener_fixture import EVENT_ID, LISTENER_NAME, ListenerFixture
from valkyrja.event.data.event_data import EventData


def test_the_defaults_are_empty() -> None:
    data = EventData()

    assert data.events == {}
    assert data.listeners == {}


def test_each_default_is_its_own_dictionary() -> None:
    EventData().events["key"] = []

    assert EventData().events == {}


def test_the_data_holds_what_the_caller_gives() -> None:
    data = EventData(events={EVENT_ID: [LISTENER_NAME]}, listeners={LISTENER_NAME: ListenerFixture})

    assert data.events == {EVENT_ID: [LISTENER_NAME]}
    assert data.listeners[LISTENER_NAME]().get_name() == LISTENER_NAME


def test_the_data_is_frozen() -> None:
    data = EventData()

    with pytest.raises(dataclasses.FrozenInstanceError):
        data.events = {}  # type: ignore[misc]
