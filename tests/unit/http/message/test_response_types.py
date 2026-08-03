#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the five kinds of response."""

import json

import pytest

from valkyrja.http.message.constant.content_type_value import ContentTypeValue
from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.response.empty_response import EmptyResponse
from valkyrja.http.message.response.html_response import HtmlResponse
from valkyrja.http.message.response.json_response import JsonResponse
from valkyrja.http.message.response.redirect_response import RedirectResponse
from valkyrja.http.message.response.text_response import TextResponse
from valkyrja.http.message.response.throwable.exception.http_invalid_redirect_status_code_exception import (
    HttpInvalidRedirectStatusCodeException,
)
from valkyrja.http.message.uri.uri import Uri


def test_an_empty_response_carries_no_content() -> None:
    response = EmptyResponse()

    assert response.get_status_code() is StatusCode.NO_CONTENT
    assert str(response.get_body()) == ""


def test_a_text_response_carries_its_text() -> None:
    response = TextResponse("hello")

    assert str(response.get_body()) == "hello"
    assert response.get_headers().get_header_line(HeaderName.CONTENT_TYPE) == ContentTypeValue.TEXT_PLAIN_UTF8
    assert response.get_status_code() is StatusCode.OK


def test_an_html_response_carries_its_html() -> None:
    response = HtmlResponse("<p>hello</p>")

    assert str(response.get_body()) == "<p>hello</p>"
    assert response.get_headers().get_header_line(HeaderName.CONTENT_TYPE) == ContentTypeValue.TEXT_HTML_UTF8


def test_a_json_response_writes_its_data() -> None:
    response = JsonResponse({"key": "value"})

    assert json.loads(str(response.get_body())) == {"key": "value"}
    assert response.get_headers().get_header_line(HeaderName.CONTENT_TYPE) == ContentTypeValue.APPLICATION_JSON
    assert response.get_data() == {"key": "value"}


def test_a_json_response_with_no_data_writes_an_empty_object() -> None:
    assert json.loads(str(JsonResponse().get_body())) == {}


def test_get_data_copies_the_data() -> None:
    response = JsonResponse({"key": "value"})

    response.get_data().clear()

    assert response.get_data() == {"key": "value"}


def test_a_response_takes_a_status_code_and_headers() -> None:
    headers = HeaderCollection(Header("X-Test", "yes"))
    response = TextResponse("hi", StatusCode.ACCEPTED, headers)

    assert response.get_status_code() is StatusCode.ACCEPTED
    assert response.get_headers().has("X-Test")


def test_a_redirect_response_writes_the_location() -> None:
    response = RedirectResponse(Uri(path="/users"))

    assert response.get_status_code() is StatusCode.FOUND
    assert response.get_headers().get_header_line(HeaderName.LOCATION) == "/users"


def test_a_redirect_response_defaults_to_the_root() -> None:
    assert RedirectResponse().get_headers().get_header_line(HeaderName.LOCATION) == "/"


def test_a_redirect_response_takes_another_redirect_code() -> None:
    response = RedirectResponse(Uri(path="/users"), StatusCode.MOVED_PERMANENTLY)

    assert response.get_status_code() is StatusCode.MOVED_PERMANENTLY


@pytest.mark.parametrize("code", [StatusCode.OK, StatusCode.NOT_FOUND, StatusCode.BAD_REQUEST])
def test_a_redirect_response_rejects_a_code_that_is_no_redirect(code: StatusCode) -> None:
    with pytest.raises(HttpInvalidRedirectStatusCodeException, match="Invalid redirect"):
        RedirectResponse(Uri(path="/users"), code)


def test_with_uri_returns_a_copy_that_points_somewhere_else() -> None:
    response = RedirectResponse(Uri(path="/users"))

    changed = response.with_uri(Uri(path="/posts"))

    assert changed.get_headers().get_header_line(HeaderName.LOCATION) == "/posts"
    assert changed.get_uri().get_path() == "/posts"
    assert response.get_headers().get_header_line(HeaderName.LOCATION) == "/users"


def test_is_redirect_reads_the_range_that_http_defines() -> None:
    assert StatusCode.MULTIPLE_CHOICES.is_redirect()
    assert StatusCode.FOUND.is_redirect()
    assert StatusCode.PERMANENT_REDIRECT.is_redirect()
    assert not StatusCode.OK.is_redirect()
    assert not StatusCode.BAD_REQUEST.is_redirect()
