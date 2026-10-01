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
from valkyrja.http.message.header.throwable.exception.http_header_invalid_value_exception import (
    HttpHeaderInvalidValueException,
)
from valkyrja.http.message.request.request import Request
from valkyrja.http.message.request.throwable.exception.http_request_invalid_request_target_exception import (
    HttpRequestInvalidRequestTargetException,
)
from valkyrja.http.message.response.empty_response import EmptyResponse
from valkyrja.http.message.response.factory.response_factory import ResponseFactory
from valkyrja.http.message.response.html_response import HtmlResponse
from valkyrja.http.message.response.json_response import JsonResponse
from valkyrja.http.message.response.redirect_response import RedirectResponse
from valkyrja.http.message.response.response import Response
from valkyrja.http.message.response.text_response import TextResponse
from valkyrja.http.message.response.throwable.exception.http_response_invalid_callback_exception import (
    HttpResponseInvalidCallbackException,
)
from valkyrja.http.message.response.throwable.exception.http_response_invalid_redirect_status_code_exception import (
    HttpResponseInvalidRedirectStatusCodeException,
)
from valkyrja.http.message.response.xml_response import XmlResponse
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
    with pytest.raises(HttpResponseInvalidRedirectStatusCodeException, match="Invalid redirect"):
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


def test_an_xml_response_carries_the_xml_and_its_content_type() -> None:
    response = XmlResponse("<a>b</a>")

    assert str(response.get_body()) == "<a>b</a>"
    assert response.get_headers().get_header_line(HeaderName.CONTENT_TYPE) == ContentTypeValue.APPLICATION_XML_UTF8


def test_a_response_builds_its_body_from_the_content() -> None:
    response = Response.create("plain", StatusCode.ACCEPTED)

    assert str(response.get_body()) == "plain"
    assert response.get_status_code() is StatusCode.ACCEPTED


def test_a_redirect_response_builds_from_a_uri() -> None:
    response = RedirectResponse.create_from_uri(Uri(path="/here"), StatusCode.MOVED_PERMANENTLY)

    assert response.get_uri().get_path() == "/here"
    assert response.get_status_code() is StatusCode.MOVED_PERMANENTLY


def test_a_json_response_builds_from_data() -> None:
    response = JsonResponse.create_from_data({"a": 1})

    assert response.get_data() == {"a": 1}


def test_a_json_response_escapes_the_characters_a_page_reads_as_markup() -> None:
    response = JsonResponse({"a": "<b>&'"})

    assert str(response.get_body()) == '{"a":"\\u003Cb\\u003E\\u0026\\u0027"}'


def test_a_json_response_leaves_a_forward_slash_as_it_is() -> None:
    assert str(JsonResponse({"p": "a/b"}).get_body()) == '{"p":"a/b"}'


def test_a_json_response_refuses_a_number_that_json_cannot_hold() -> None:
    with pytest.raises(ValueError, match="Out of range float"):
        JsonResponse({"a": float("nan")})


def test_a_json_response_reads_its_body_as_json() -> None:
    response = JsonResponse({"a": [1, 2]})

    assert response.get_body_as_json() == {"a": [1, 2]}


def test_with_json_as_body_replaces_the_data() -> None:
    response = JsonResponse({"a": 1})

    changed = response.with_json_as_body({"b": 2})

    assert changed.get_data() == {"b": 2}
    assert changed.get_body_as_json() == {"b": 2}
    assert response.get_data() == {"a": 1}


def test_the_data_of_a_json_response_is_a_deep_copy() -> None:
    nested = {"a": [1]}
    response = JsonResponse(nested)

    nested["a"].append(2)
    response.get_data()["a"].append(3)

    assert response.get_body_as_json() == {"a": [1]}


def test_with_callback_wraps_the_json_in_the_callback() -> None:
    response = JsonResponse({"a": 1}).with_callback("handle")

    assert str(response.get_body()) == '/**/handle({"a":1});'
    assert response.get_headers().get_header_line(HeaderName.CONTENT_TYPE) == ContentTypeValue.TEXT_JAVASCRIPT


def test_with_callback_takes_a_name_that_holds_several_parts() -> None:
    response = JsonResponse({"a": 1}).with_callback("app.handle")

    assert str(response.get_body()) == '/**/app.handle({"a":1});'


@pytest.mark.parametrize("callback", ["", "1bad", "a b", "a..b", "a.", "with-dash"])
def test_with_callback_refuses_a_name_javascript_cannot_call(callback: str) -> None:
    with pytest.raises(HttpResponseInvalidCallbackException, match="not valid"):
        JsonResponse({"a": 1}).with_callback(callback)


def test_without_callback_writes_the_json_alone() -> None:
    response = JsonResponse({"a": 1}).with_callback("handle").without_callback()

    assert str(response.get_body()) == '{"a":1}'
    assert response.get_headers().get_header_line(HeaderName.CONTENT_TYPE) == ContentTypeValue.APPLICATION_JSON


def test_the_response_factory_builds_each_kind() -> None:
    factory = ResponseFactory()

    assert isinstance(factory.create_response("a"), Response)
    assert isinstance(factory.create_text_response("a"), TextResponse)
    assert isinstance(factory.create_json_response({"a": 1}), JsonResponse)
    assert isinstance(factory.create_jsonp_response("handle", {"a": 1}), JsonResponse)
    assert isinstance(factory.create_redirect_response("/here"), RedirectResponse)


def test_the_response_factory_wraps_the_jsonp_callback() -> None:
    response = ResponseFactory().create_jsonp_response("handle", {"a": 1})

    assert str(response.get_body()) == '/**/handle({"a":1});'


def test_the_response_factory_reads_the_redirect_uri() -> None:
    response = ResponseFactory().create_redirect_response("/here")

    assert response.get_headers().get_header_line(HeaderName.LOCATION) == "/here"


def test_an_empty_reason_phrase_falls_back_to_the_one_the_code_names() -> None:
    response = Response(status_code=StatusCode.NOT_FOUND).with_reason_phrase("")

    assert response.get_reason_phrase() == StatusCode.NOT_FOUND.as_phrase()


def test_a_reason_phrase_that_would_split_the_response_is_refused() -> None:
    with pytest.raises(HttpHeaderInvalidValueException):
        Response().with_reason_phrase("OK\r\nX-Injected: yes")


def test_a_request_refuses_a_request_target_that_holds_whitespace() -> None:
    with pytest.raises(HttpRequestInvalidRequestTargetException, match="cannot contain whitespace"):
        Request().with_request_target("/a b")


def test_a_request_takes_a_request_target_with_no_whitespace() -> None:
    assert Request().with_request_target("/a?b=c").get_request_target() == "/a?b=c"
