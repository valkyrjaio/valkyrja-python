#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ValkyrjaInvalidArgumentException base class."""

import re

import pytest

from tests.fixtures.throwable.exception.valkyrja_invalid_argument_exception_fixture import (
    ValkyrjaInvalidArgumentExceptionFixture,
)
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable
from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)

# The MD5 hexadecimal digest that a trace code is.
TRACE_CODE_PATTERN = re.compile(r"[0-9a-f]{32}")


def test_the_base_class_does_not_construct() -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable ValkyrjaInvalidArgumentException"):
        ValkyrjaInvalidArgumentException()


def test_get_trace_code() -> None:
    exception = ValkyrjaInvalidArgumentExceptionFixture()

    assert TRACE_CODE_PATTERN.fullmatch(exception.get_trace_code())
    assert exception.get_trace_code() == exception.get_trace_code()


def test_a_concrete_exception_is_a_value_error() -> None:
    with pytest.raises(ValueError, match="Custom message"):
        raise ValkyrjaInvalidArgumentExceptionFixture("Custom message")


def test_a_concrete_exception_implements_the_contract() -> None:
    assert isinstance(ValkyrjaInvalidArgumentExceptionFixture(), ValkyrjaThrowable)
