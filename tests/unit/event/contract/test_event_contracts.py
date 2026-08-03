#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the contracts that an event implements."""

import pytest

from tests.fixtures.event.data.event_fixture import EventFixture
from valkyrja.event.contract.arguments_capable_event_contract import ArgumentsCapableEventContract
from valkyrja.event.contract.dispatch_collectable_event_contract import (
    DispatchCollectableEventContract,
)


def test_the_arguments_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        ArgumentsCapableEventContract()  # type: ignore[abstract]


def test_the_dispatch_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        DispatchCollectableEventContract()  # type: ignore[abstract]


def test_set_arguments_returns_the_event() -> None:
    event = EventFixture()

    assert event.set_arguments({"key": "value"}) is event
    assert event.arguments == {"key": "value"}


def test_the_event_keeps_each_dispatch() -> None:
    event = EventFixture()

    event.add_dispatch("first")
    event.add_dispatch("second")

    assert event.get_dispatches() == ["first", "second"]


def test_a_new_event_has_no_dispatch() -> None:
    assert EventFixture().get_dispatches() == []
