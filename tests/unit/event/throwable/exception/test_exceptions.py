#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the exception hierarchy of the Event component."""

import pytest

from valkyrja.event.throwable.contract.event_throwable import EventThrowable
from valkyrja.event.throwable.exception.abstract.event_invalid_argument_exception import (
    EventInvalidArgumentException,
)
from valkyrja.event.throwable.exception.abstract.event_runtime_exception import EventRuntimeException
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable

ABSTRACT_EXCEPTIONS = [EventThrowable, EventRuntimeException, EventInvalidArgumentException]


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_an_abstract_exception_does_not_construct(exception_class: type[ValkyrjaThrowable]) -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable"):
        exception_class()


def test_the_runtime_base_extends_the_language_root() -> None:
    assert issubclass(EventRuntimeException, RuntimeError)
    assert issubclass(EventRuntimeException, EventThrowable)
    assert issubclass(EventRuntimeException, ValkyrjaThrowable)


def test_the_invalid_argument_base_extends_the_language_root() -> None:
    assert issubclass(EventInvalidArgumentException, ValueError)
    assert issubclass(EventInvalidArgumentException, EventThrowable)
    assert issubclass(EventInvalidArgumentException, ValkyrjaThrowable)
