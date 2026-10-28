#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ThrowableHandlerContract."""

import pytest

from tests.fixtures.throwable.handler.throwable_handler_fixture import ThrowableHandlerFixture
from valkyrja.throwable.handler.contract.throwable_handler_contract import ThrowableHandlerContract


def test_the_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        ThrowableHandlerContract()  # type: ignore[abstract]


def test_enable_defaults_to_hidden_errors() -> None:
    handler = ThrowableHandlerFixture()

    handler.enable()

    assert handler.enabled
    assert not handler.display_errors


def test_enable_displays_errors_when_asked() -> None:
    handler = ThrowableHandlerFixture()

    handler.enable(display_errors=True)

    assert handler.enabled
    assert handler.display_errors


def test_the_fixture_implements_the_contract() -> None:
    assert isinstance(ThrowableHandlerFixture(), ThrowableHandlerContract)
