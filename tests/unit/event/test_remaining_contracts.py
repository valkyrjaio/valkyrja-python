#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Event contracts that the implementation pass fills in.

Each contract here has no implementation yet. The test pins that the contract is
abstract, so a later change cannot make it constructible without a failure.
"""

import inspect

import pytest

from valkyrja.event.collection.contract.listener_collection_contract import (
    ListenerCollectionContract,
)
from valkyrja.event.collector.contract.listener_collector_contract import ListenerCollectorContract
from valkyrja.event.dispatcher.contract.event_dispatcher_contract import EventDispatcherContract

CONTRACTS = [ListenerCollectionContract, ListenerCollectorContract, EventDispatcherContract]


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_does_not_construct(contract: type) -> None:
    with pytest.raises(TypeError, match="abstract"):
        contract()


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_declares_an_abstract_method(contract: type) -> None:
    assert inspect.isabstract(contract)
