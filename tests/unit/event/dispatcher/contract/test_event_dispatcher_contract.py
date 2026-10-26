#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for EventDispatcherContract.

The contract has no implementation yet, so the test pins that it stays abstract.
"""

import inspect

import pytest

from valkyrja.event.dispatcher.contract.event_dispatcher_contract import EventDispatcherContract


def test_the_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        EventDispatcherContract()  # type: ignore[abstract]


def test_the_contract_declares_an_abstract_method() -> None:
    assert inspect.isabstract(EventDispatcherContract)
