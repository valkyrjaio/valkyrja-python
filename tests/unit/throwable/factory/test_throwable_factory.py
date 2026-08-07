#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for ThrowableFactory."""

import re

from tests.fixtures.throwable.exception.valkyrja_invalid_argument_exception_fixture import (
    ValkyrjaInvalidArgumentExceptionFixture,
)
from tests.fixtures.throwable.exception.valkyrja_runtime_exception_fixture import (
    ValkyrjaRuntimeExceptionFixture,
)
from valkyrja.throwable.factory.throwable_factory import ThrowableFactory

# The MD5 hexadecimal digest that the factory returns.
TRACE_CODE_PATTERN = re.compile(r"[0-9a-f]{32}")


def test_get_trace_code() -> None:
    exception = ValkyrjaRuntimeExceptionFixture()
    exception2 = ValkyrjaRuntimeExceptionFixture()
    exception3 = ValkyrjaRuntimeExceptionFixture("Custom message")

    trace_code = ThrowableFactory.get_trace_code(exception)
    trace_code2 = ThrowableFactory.get_trace_code(exception2)
    trace_code3 = ThrowableFactory.get_trace_code(exception3)

    assert trace_code == trace_code2
    assert trace_code == trace_code3
    assert trace_code2 == trace_code3


def test_get_trace_code_has_the_digest_format() -> None:
    assert TRACE_CODE_PATTERN.fullmatch(ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture()))


def test_get_trace_code_differs_for_a_different_class() -> None:
    runtime_trace_code = ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture())
    invalid_argument_trace_code = ThrowableFactory.get_trace_code(ValkyrjaInvalidArgumentExceptionFixture())

    assert runtime_trace_code != invalid_argument_trace_code


def test_get_trace_code_differs_once_the_throwable_carries_a_trace() -> None:
    unraised_trace_code = ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture())

    try:
        raise ValkyrjaRuntimeExceptionFixture
    except ValkyrjaRuntimeExceptionFixture as exception:
        raised_trace_code = ThrowableFactory.get_trace_code(exception)

    assert raised_trace_code != unraised_trace_code


def test_get_trace_code_accepts_a_throwable_the_framework_does_not_define() -> None:
    assert TRACE_CODE_PATTERN.fullmatch(ThrowableFactory.get_trace_code(ValueError("Custom message")))
