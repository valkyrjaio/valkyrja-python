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
from valkyrja.http.message.header.throwable.exception.http_header_invalid_cookie_exception import (
    HttpHeaderInvalidCookieException,
)
from valkyrja.http.message.header.throwable.exception.http_header_invalid_header_name_exception import (
    HttpHeaderInvalidHeaderNameException,
)
from valkyrja.http.message.header.throwable.exception.http_header_invalid_header_param_exception import (
    HttpHeaderInvalidHeaderParamException,
)
from valkyrja.http.message.header.throwable.exception.http_header_invalid_name_exception import (
    HttpHeaderInvalidNameException,
)
from valkyrja.http.message.header.throwable.exception.http_header_invalid_value_exception import (
    HttpHeaderInvalidValueException,
)
from valkyrja.http.message.header.throwable.exception.http_header_unsupported_offset_set_exception import (
    HttpHeaderUnsupportedOffsetSetException,
)
from valkyrja.http.message.header.throwable.exception.http_header_unsupported_offset_unset_exception import (
    HttpHeaderUnsupportedOffsetUnsetException,
)
from valkyrja.http.message.request.throwable.contract.http_request_throwable import HttpRequestThrowable
from valkyrja.http.message.request.throwable.exception.abstract.http_request_invalid_argument_exception import (
    HttpRequestInvalidArgumentException,
)
from valkyrja.http.message.request.throwable.exception.abstract.http_request_runtime_exception import (
    HttpRequestRuntimeException,
)
from valkyrja.http.message.request.throwable.exception.http_request_invalid_request_target_exception import (
    HttpRequestInvalidRequestTargetException,
)
from valkyrja.http.message.response.throwable.contract.http_response_throwable import HttpResponseThrowable
from valkyrja.http.message.response.throwable.exception.abstract.http_response_invalid_argument_exception import (
    HttpResponseInvalidArgumentException,
)
from valkyrja.http.message.response.throwable.exception.abstract.http_response_runtime_exception import (
    HttpResponseRuntimeException,
)
from valkyrja.http.message.response.throwable.exception.http_response_invalid_callback_exception import (
    HttpResponseInvalidCallbackException,
)
from valkyrja.http.message.response.throwable.exception.http_response_invalid_redirect_status_code_exception import (
    HttpResponseInvalidRedirectStatusCodeException,
)
from valkyrja.http.message.stream.throwable.contract.http_stream_throwable import HttpStreamThrowable
from valkyrja.http.message.stream.throwable.exception.abstract.http_stream_invalid_argument_exception import (
    HttpStreamInvalidArgumentException,
)
from valkyrja.http.message.stream.throwable.exception.abstract.http_stream_runtime_exception import (
    HttpStreamRuntimeException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_invalid_length_exception import (
    HttpStreamInvalidLengthException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_invalid_stream_exception import (
    HttpStreamInvalidStreamException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_no_stream_available_exception import (
    HttpStreamNoStreamAvailableException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_read_exception import (
    HttpStreamStreamReadException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_seek_exception import (
    HttpStreamStreamSeekException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_tell_exception import (
    HttpStreamStreamTellException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_write_exception import (
    HttpStreamStreamWriteException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_unreadable_stream_exception import (
    HttpStreamUnreadableStreamException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_unseekable_stream_exception import (
    HttpStreamUnseekableStreamException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_unwritable_stream_exception import (
    HttpStreamUnwritableStreamException,
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
from valkyrja.http.message.uri.throwable.exception.http_uri_invalid_from_string_exception import (
    HttpUriInvalidFromStringException,
)
from valkyrja.http.message.uri.throwable.exception.http_uri_invalid_path_exception import (
    HttpUriInvalidPathException,
)
from valkyrja.http.message.uri.throwable.exception.http_uri_invalid_port_exception import (
    HttpUriInvalidPortException,
)
from valkyrja.http.message.uri.throwable.exception.http_uri_invalid_query_exception import (
    HttpUriInvalidQueryException,
)
from valkyrja.http.message.uri.throwable.exception.http_uri_invalid_scheme_exception import (
    HttpUriInvalidSchemeException,
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


CONCRETE_EXCEPTIONS = [
    (HttpHeaderInvalidCookieException, HttpHeaderThrowable, HttpHeaderInvalidArgumentException),
    (HttpHeaderInvalidHeaderNameException, HttpHeaderThrowable, HttpHeaderInvalidArgumentException),
    (HttpHeaderInvalidHeaderParamException, HttpHeaderThrowable, HttpHeaderInvalidArgumentException),
    (HttpHeaderInvalidNameException, HttpHeaderThrowable, HttpHeaderInvalidArgumentException),
    (HttpHeaderInvalidValueException, HttpHeaderThrowable, HttpHeaderInvalidArgumentException),
    (HttpHeaderUnsupportedOffsetSetException, HttpHeaderThrowable, HttpHeaderRuntimeException),
    (HttpHeaderUnsupportedOffsetUnsetException, HttpHeaderThrowable, HttpHeaderRuntimeException),
    (HttpRequestInvalidRequestTargetException, HttpRequestThrowable, HttpRequestInvalidArgumentException),
    (HttpResponseInvalidCallbackException, HttpResponseThrowable, HttpResponseInvalidArgumentException),
    (HttpResponseInvalidRedirectStatusCodeException, HttpResponseThrowable, HttpResponseInvalidArgumentException),
    (HttpStreamInvalidLengthException, HttpStreamThrowable, HttpStreamInvalidArgumentException),
    (HttpStreamInvalidStreamException, HttpStreamThrowable, HttpStreamInvalidArgumentException),
    (HttpStreamNoStreamAvailableException, HttpStreamThrowable, HttpStreamRuntimeException),
    (HttpStreamStreamReadException, HttpStreamThrowable, HttpStreamRuntimeException),
    (HttpStreamStreamSeekException, HttpStreamThrowable, HttpStreamRuntimeException),
    (HttpStreamStreamTellException, HttpStreamThrowable, HttpStreamRuntimeException),
    (HttpStreamStreamWriteException, HttpStreamThrowable, HttpStreamRuntimeException),
    (HttpStreamUnreadableStreamException, HttpStreamThrowable, HttpStreamRuntimeException),
    (HttpStreamUnseekableStreamException, HttpStreamThrowable, HttpStreamRuntimeException),
    (HttpStreamUnwritableStreamException, HttpStreamThrowable, HttpStreamRuntimeException),
    (HttpUriInvalidFromStringException, HttpUriThrowable, HttpUriInvalidArgumentException),
    (HttpUriInvalidPathException, HttpUriThrowable, HttpUriInvalidArgumentException),
    (HttpUriInvalidPortException, HttpUriThrowable, HttpUriInvalidArgumentException),
    (HttpUriInvalidQueryException, HttpUriThrowable, HttpUriInvalidArgumentException),
    (HttpUriInvalidSchemeException, HttpUriThrowable, HttpUriInvalidArgumentException),
]


@pytest.mark.parametrize(("exception_class", "throwable_class", "base_class"), CONCRETE_EXCEPTIONS)
def test_every_concrete_exception_narrows_its_sub_component_and_keeps_its_category(
    exception_class: type, throwable_class: type, base_class: type
) -> None:
    # A concrete exception declares no executable line, so only this assertion
    # catches one that points at another sub-component or another category.
    assert issubclass(exception_class, throwable_class)
    assert issubclass(exception_class, base_class)
