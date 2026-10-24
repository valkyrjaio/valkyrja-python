#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the exception hierarchy of the Http component."""

import pytest

from valkyrja.http.message.throwable.contract.http_message_throwable import HttpMessageThrowable
from valkyrja.http.message.throwable.exception.abstract.http_message_invalid_argument_exception import (
    HttpMessageInvalidArgumentException,
)
from valkyrja.http.message.throwable.exception.abstract.http_message_runtime_exception import (
    HttpMessageRuntimeException,
)
from valkyrja.http.throwable.contract.http_throwable import HttpThrowable
from valkyrja.http.throwable.exception.abstract.http_invalid_argument_exception import (
    HttpInvalidArgumentException,
)
from valkyrja.http.throwable.exception.abstract.http_runtime_exception import HttpRuntimeException
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable

ABSTRACT_EXCEPTIONS = [
    HttpThrowable,
    HttpRuntimeException,
    HttpInvalidArgumentException,
    HttpMessageThrowable,
    HttpMessageRuntimeException,
    HttpMessageInvalidArgumentException,
]


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_an_abstract_exception_does_not_construct(exception_class: type[ValkyrjaThrowable]) -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable"):
        exception_class()


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_every_exception_narrows_the_http_throwable(exception_class: type) -> None:
    assert issubclass(exception_class, HttpThrowable)


def test_the_message_throwable_narrows_the_http_throwable() -> None:
    assert issubclass(HttpMessageThrowable, HttpThrowable)


def test_the_bases_extend_the_language_roots() -> None:
    assert issubclass(HttpRuntimeException, RuntimeError)
    assert issubclass(HttpInvalidArgumentException, ValueError)
    assert issubclass(HttpMessageRuntimeException, RuntimeError)
    assert issubclass(HttpMessageInvalidArgumentException, ValueError)
