#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the exception hierarchy of the Container component."""

import pytest

from valkyrja.container.throwable.contract.container_throwable import ContainerThrowable
from valkyrja.container.throwable.exception.abstract.container_invalid_argument_exception import (
    ContainerInvalidArgumentException,
)
from valkyrja.container.throwable.exception.abstract.container_runtime_exception import (
    ContainerRuntimeException,
)
from valkyrja.container.throwable.exception.container_invalid_publish_callback_exception import (
    ContainerInvalidPublishCallbackException,
)
from valkyrja.container.throwable.exception.container_invalid_reference_exception import (
    ContainerInvalidReferenceException,
)
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable
from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import ValkyrjaRuntimeException

SERVICE_ID = "tests.unit.container.Service"

ABSTRACT_EXCEPTIONS = [
    ContainerThrowable,
    ContainerRuntimeException,
    ContainerInvalidArgumentException,
]


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_an_abstract_exception_does_not_construct(exception_class: type[ValkyrjaThrowable]) -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable"):
        exception_class()


def test_the_invalid_reference_exception_names_the_id() -> None:
    exception = ContainerInvalidReferenceException(SERVICE_ID)

    assert str(exception) == f"Service with `{SERVICE_ID}` not found"


def test_the_invalid_reference_exception_extends_the_invalid_argument_base() -> None:
    exception = ContainerInvalidReferenceException(SERVICE_ID)

    assert isinstance(exception, ContainerInvalidArgumentException)
    assert isinstance(exception, ValkyrjaInvalidArgumentException)
    assert isinstance(exception, ContainerThrowable)
    assert isinstance(exception, ValkyrjaThrowable)
    assert isinstance(exception, ValueError)


def test_the_invalid_publish_callback_exception_extends_the_runtime_base() -> None:
    exception = ContainerInvalidPublishCallbackException("Custom message")

    assert isinstance(exception, ContainerRuntimeException)
    assert isinstance(exception, ValkyrjaRuntimeException)
    assert isinstance(exception, ContainerThrowable)
    assert isinstance(exception, ValkyrjaThrowable)
    assert isinstance(exception, RuntimeError)
    assert str(exception) == "Custom message"


def test_a_concrete_exception_gets_a_trace_code() -> None:
    assert ContainerInvalidReferenceException(SERVICE_ID).get_trace_code()
