#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the contracts that an event implements."""

import pytest

from tests.fixtures.event.data.event_fixture import EVENT_ID, EventFixture
from tests.fixtures.event.data.stoppable_event_fixture import StoppableEventFixture
from valkyrja.event.contract.arguments_capable_event_contract import ArgumentsCapableEventContract
from valkyrja.event.contract.dispatch_collectable_event_contract import (
    DispatchCollectableEventContract,
)
from valkyrja.event.contract.event_contract import EventContract
from valkyrja.event.contract.stoppable_event_contract import StoppableEventContract

CONTRACTS = [
    EventContract,
    ArgumentsCapableEventContract,
    DispatchCollectableEventContract,
    StoppableEventContract,
]


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_does_not_construct(contract: type) -> None:
    with pytest.raises(TypeError, match="abstract"):
        contract()


@pytest.mark.parametrize("contract", CONTRACTS)
def test_every_event_contract_extends_the_event_contract(contract: type) -> None:
    assert issubclass(contract, EventContract)


def test_an_event_states_its_own_id() -> None:
    assert EventFixture().get_event_id() == EVENT_ID


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


def test_a_stoppable_event_reports_whether_it_stopped() -> None:
    event = StoppableEventFixture()

    assert not event.is_propagation_stopped()

    event.stop()

    assert event.is_propagation_stopped()
