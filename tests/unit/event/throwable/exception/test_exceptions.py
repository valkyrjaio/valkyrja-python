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
from valkyrja.event.throwable.exception.event_invalid_event_exception import (
    EventInvalidEventException,
)
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


def test_the_invalid_event_exception_names_the_id() -> None:
    exception = EventInvalidEventException("Valkyrja.Tests.NotAnEvent")

    assert str(exception) == "Service with `Valkyrja.Tests.NotAnEvent` is not an event"
    assert exception.get_id() == "Valkyrja.Tests.NotAnEvent"
    assert isinstance(exception, EventInvalidArgumentException)
