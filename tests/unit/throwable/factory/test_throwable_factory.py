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


def test_get_trace_code_matches_for_one_construction_site() -> None:
    # Both throwables are constructed on one line, so both share a whole stack.
    trace_codes = [ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture()) for _ in range(2)]

    assert trace_codes[0] == trace_codes[1]


def test_get_trace_code_ignores_the_message() -> None:
    trace_codes = [
        ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture(message)) for message in ("", "Custom message")
    ]

    assert trace_codes[0] == trace_codes[1]


def test_get_trace_code_has_the_digest_format() -> None:
    assert TRACE_CODE_PATTERN.fullmatch(ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture()))


def test_get_trace_code_differs_for_a_different_class() -> None:
    runtime_trace_code = ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture())
    invalid_argument_trace_code = ThrowableFactory.get_trace_code(ValkyrjaInvalidArgumentExceptionFixture())

    assert runtime_trace_code != invalid_argument_trace_code


def test_get_trace_code_differs_for_two_construction_sites() -> None:
    trace_code = ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture())
    trace_code2 = ThrowableFactory.get_trace_code(ValkyrjaRuntimeExceptionFixture())

    assert trace_code != trace_code2


def test_get_trace_code_holds_across_a_raise_and_a_re_raise() -> None:
    exception = ValkyrjaRuntimeExceptionFixture()
    constructed_trace_code = ThrowableFactory.get_trace_code(exception)

    try:
        try:
            raise exception
        except ValkyrjaRuntimeExceptionFixture:
            raise
    except ValkyrjaRuntimeExceptionFixture as raised:
        assert ThrowableFactory.get_trace_code(raised) == constructed_trace_code


def test_get_trace_code_accepts_a_throwable_the_framework_does_not_define() -> None:
    assert TRACE_CODE_PATTERN.fullmatch(ThrowableFactory.get_trace_code(ValueError("Custom message")))
