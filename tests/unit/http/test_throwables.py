#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the exception hierarchy of the Http component."""

import pytest

from valkyrja.http.message.header.throwable.contract.http_header_throwable import HttpHeaderThrowable
from valkyrja.http.message.header.throwable.exception.abstract.http_header_invalid_argument_exception import (
    HttpHeaderInvalidArgumentException,
)
from valkyrja.http.message.header.throwable.exception.abstract.http_header_runtime_exception import (
    HttpHeaderRuntimeException,
)
from valkyrja.http.message.request.throwable.contract.http_request_throwable import HttpRequestThrowable
from valkyrja.http.message.request.throwable.exception.abstract.http_request_invalid_argument_exception import (
    HttpRequestInvalidArgumentException,
)
from valkyrja.http.message.request.throwable.exception.abstract.http_request_runtime_exception import (
    HttpRequestRuntimeException,
)
from valkyrja.http.message.response.throwable.contract.http_response_throwable import HttpResponseThrowable
from valkyrja.http.message.response.throwable.exception.abstract.http_response_invalid_argument_exception import (
    HttpResponseInvalidArgumentException,
)
from valkyrja.http.message.response.throwable.exception.abstract.http_response_runtime_exception import (
    HttpResponseRuntimeException,
)
from valkyrja.http.message.stream.throwable.contract.http_stream_throwable import HttpStreamThrowable
from valkyrja.http.message.stream.throwable.exception.abstract.http_stream_invalid_argument_exception import (
    HttpStreamInvalidArgumentException,
)
from valkyrja.http.message.stream.throwable.exception.abstract.http_stream_runtime_exception import (
    HttpStreamRuntimeException,
)
from valkyrja.http.message.throwable.contract.http_message_throwable import HttpMessageThrowable
from valkyrja.http.message.throwable.exception.abstract.http_message_invalid_argument_exception import (
    HttpMessageInvalidArgumentException,
)
from valkyrja.http.message.throwable.exception.abstract.http_message_runtime_exception import (
    HttpMessageRuntimeException,
)
from valkyrja.http.message.uri.throwable.contract.http_uri_throwable import HttpUriThrowable
from valkyrja.http.message.uri.throwable.exception.abstract.http_uri_invalid_argument_exception import (
    HttpUriInvalidArgumentException,
)
from valkyrja.http.message.uri.throwable.exception.abstract.http_uri_runtime_exception import (
    HttpUriRuntimeException,
)
from valkyrja.http.throwable.contract.http_throwable import HttpThrowable
from valkyrja.http.throwable.exception.abstract.http_invalid_argument_exception import (
    HttpInvalidArgumentException,
)
from valkyrja.http.throwable.exception.abstract.http_runtime_exception import HttpRuntimeException
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable

SUB_COMPONENT_THROWABLES = [
    HttpHeaderThrowable,
    HttpRequestThrowable,
    HttpResponseThrowable,
    HttpStreamThrowable,
    HttpUriThrowable,
]

RUNTIME_BASES = [
    HttpRuntimeException,
    HttpMessageRuntimeException,
    HttpHeaderRuntimeException,
    HttpRequestRuntimeException,
    HttpResponseRuntimeException,
    HttpStreamRuntimeException,
    HttpUriRuntimeException,
]

INVALID_ARGUMENT_BASES = [
    HttpInvalidArgumentException,
    HttpMessageInvalidArgumentException,
    HttpHeaderInvalidArgumentException,
    HttpRequestInvalidArgumentException,
    HttpResponseInvalidArgumentException,
    HttpStreamInvalidArgumentException,
    HttpUriInvalidArgumentException,
]

ABSTRACT_EXCEPTIONS = [
    HttpThrowable,
    HttpMessageThrowable,
    *SUB_COMPONENT_THROWABLES,
    *RUNTIME_BASES,
    *INVALID_ARGUMENT_BASES,
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


@pytest.mark.parametrize("throwable_class", SUB_COMPONENT_THROWABLES)
def test_every_sub_component_throwable_narrows_the_message_throwable(throwable_class: type) -> None:
    assert issubclass(throwable_class, HttpMessageThrowable)


@pytest.mark.parametrize("exception_class", RUNTIME_BASES)
def test_every_runtime_base_extends_the_language_root(exception_class: type) -> None:
    assert issubclass(exception_class, RuntimeError)


@pytest.mark.parametrize("exception_class", INVALID_ARGUMENT_BASES)
def test_every_invalid_argument_base_extends_the_language_root(exception_class: type) -> None:
    assert issubclass(exception_class, ValueError)
