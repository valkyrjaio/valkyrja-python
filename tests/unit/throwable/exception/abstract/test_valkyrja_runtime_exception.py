#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ValkyrjaRuntimeException base class."""

import re

import pytest

from tests.fixtures.throwable.exception.valkyrja_runtime_exception_fixture import (
    ValkyrjaRuntimeExceptionFixture,
)
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import ValkyrjaRuntimeException

# The MD5 hexadecimal digest that a trace code is.
TRACE_CODE_PATTERN = re.compile(r"[0-9a-f]{32}")


def test_the_base_class_does_not_construct() -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable ValkyrjaRuntimeException"):
        ValkyrjaRuntimeException()


def test_get_trace_code() -> None:
    exception = ValkyrjaRuntimeExceptionFixture()

    assert TRACE_CODE_PATTERN.fullmatch(exception.get_trace_code())
    assert exception.get_trace_code() == exception.get_trace_code()


def test_a_concrete_exception_is_a_runtime_error() -> None:
    with pytest.raises(RuntimeError):
        raise ValkyrjaRuntimeExceptionFixture("Custom message")


def test_a_concrete_exception_implements_the_contract() -> None:
    assert isinstance(ValkyrjaRuntimeExceptionFixture(), ValkyrjaThrowable)


def test_a_concrete_exception_is_an_exception() -> None:
    with pytest.raises(Exception, match="Custom message"):
        raise ValkyrjaRuntimeExceptionFixture("Custom message")
