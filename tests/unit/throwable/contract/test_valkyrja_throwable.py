#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ValkyrjaThrowable contract."""

import pytest

from tests.fixtures.throwable.exception.valkyrja_throwable_fixture import ValkyrjaThrowableFixture
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable


def test_the_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable ValkyrjaThrowable"):
        ValkyrjaThrowable()  # type: ignore[abstract]


def test_a_concrete_throwable_constructs() -> None:
    throwable = ValkyrjaThrowableFixture("Custom message")

    assert isinstance(throwable, ValkyrjaThrowable)
    assert throwable.args == ("Custom message",)


def test_a_concrete_throwable_raises() -> None:
    with pytest.raises(ValkyrjaThrowable) as exception_info:
        raise ValkyrjaThrowableFixture("Custom message")

    assert str(exception_info.value) == "Custom message"


def test_a_concrete_throwable_is_a_base_exception() -> None:
    assert isinstance(ValkyrjaThrowableFixture(), BaseException)


def test_a_concrete_throwable_gets_a_trace_code() -> None:
    assert ValkyrjaThrowableFixture().get_trace_code()
