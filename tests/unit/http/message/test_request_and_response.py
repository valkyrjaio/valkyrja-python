#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Request and the Response."""

from typing import Any

from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.protocol_version import ProtocolVersion
from valkyrja.http.message.enum.request_method import RequestMethod
from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.enum.status_text import StatusText
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.header.value.cookie import Cookie
from valkyrja.http.message.request.request import Request
from valkyrja.http.message.response.response import Response
from valkyrja.http.message.stream.stream import Stream
from valkyrja.http.message.uri.enum.scheme import Scheme
from valkyrja.http.message.uri.uri import Uri


def make_body(text: str) -> Stream:
    stream = Stream()
    stream.write(text)
    stream.rewind()

    return stream


def test_a_new_request_has_defaults() -> None:
    request = Request()

    assert request.get_method() is RequestMethod.GET
    assert request.get_protocol_version() is ProtocolVersion.V1_1
    assert request.get_request_target() == "/"


def test_a_request_adds_the_host_header_from_the_uri() -> None:
    request = Request(uri=Uri(scheme=Scheme.HTTP, host="valkyrja.io"))

    assert request.get_headers().get_header_line(HeaderName.HOST) == "valkyrja.io:80"


def test_a_request_keeps_a_host_header_that_the_caller_gave() -> None:
    request = Request(
        uri=Uri(host="valkyrja.io"),
        headers=HeaderCollection(Header(HeaderName.HOST, "other.io")),
    )

    assert request.get_headers().get_header_line(HeaderName.HOST) == "other.io"


def test_a_request_with_no_host_adds_no_header() -> None:
    assert not Request().get_headers().has(HeaderName.HOST)


def test_the_request_target_reads_the_path_and_the_query() -> None:
    request = Request(uri=Uri(path="/users", query="page=2"))

    assert request.get_request_target() == "/users?page=2"


def test_the_request_target_reads_the_path_alone() -> None:
    assert Request(uri=Uri(path="/users")).get_request_target() == "/users"


def test_with_request_target_wins_over_the_uri() -> None:
    request = Request(uri=Uri(path="/users")).with_request_target("*")

    assert request.get_request_target() == "*"


def test_with_method_returns_a_copy() -> None:
    request = Request()

    assert request.with_method(RequestMethod.POST).get_method() is RequestMethod.POST
    assert request.get_method() is RequestMethod.GET


def test_with_uri_sets_the_host_header() -> None:
    request = Request().with_uri(Uri(host="valkyrja.io", port=8080))

    assert request.get_headers().get_header_line(HeaderName.HOST) == "valkyrja.io:8080"


def test_with_uri_preserves_the_host_header_when_asked() -> None:
    request = Request(uri=Uri(host="first.io"), headers=HeaderCollection(Header(HeaderName.HOST, "first.io")))

    changed = request.with_uri(Uri(host="second.io"), preserve_host=True)

    assert changed.get_headers().get_header_line(HeaderName.HOST) == "first.io"
    assert changed.get_uri().get_host() == "second.io"


def test_with_uri_that_has_no_host_leaves_the_header_alone() -> None:
    request = Request().with_uri(Uri(path="/users"))

    assert not request.get_headers().has(HeaderName.HOST)


def test_the_message_setters_return_copies() -> None:
    request = Request()
    body = make_body("hello")
    headers = HeaderCollection(Header("Accept", "text/html"))

    assert request.with_body(body).get_body() is body
    assert request.with_headers(headers).get_headers() is headers
    assert request.with_protocol_version(ProtocolVersion.V2).get_protocol_version() is ProtocolVersion.V2
    assert request.get_protocol_version() is ProtocolVersion.V1_1


def test_a_new_response_is_ok() -> None:
    response = Response()

    assert response.get_status_code() is StatusCode.OK
    assert response.get_reason_phrase() == "OK"


def test_every_status_code_has_a_phrase() -> None:
    for code in StatusCode:
        assert code.as_phrase() == StatusText[code.name].value


def test_with_status_code_updates_the_phrase() -> None:
    response = Response().with_status_code(StatusCode.NOT_FOUND)

    assert response.get_status_code() is StatusCode.NOT_FOUND
    assert response.get_reason_phrase() == "Not Found"


def test_with_reason_phrase_returns_a_copy() -> None:
    response = Response()

    assert response.with_reason_phrase("Custom").get_reason_phrase() == "Custom"
    assert response.get_reason_phrase() == "OK"


def test_with_cookie_adds_a_set_cookie_header() -> None:
    response = Response().with_cookie(Cookie("session", "abc"))

    assert "session=abc" in response.get_headers().get_header_line(HeaderName.SET_COOKIE)


def test_with_cookie_keeps_each_cookie_as_its_own_value() -> None:
    """A cookie with no value writes the name alone, the same as PHP does."""
    response = Response().with_cookie(Cookie("first")).with_cookie(Cookie("second"))

    assert len(response.get_headers().get(HeaderName.SET_COOKIE).get_values()) == 2


def test_send_headers_writes_each_cookie_on_its_own_line(capsys: Any) -> None:
    """RFC 7230 forbids joining a `Set-Cookie` field with a comma."""
    response = Response().with_cookie(Cookie("first")).with_cookie(Cookie("second"))

    response.send_headers()

    lines = [line for line in capsys.readouterr().out.splitlines() if line != ""]

    assert len(lines) == 2
    assert lines[0].startswith("Set-Cookie: first;")
    assert lines[1].startswith("Set-Cookie: second;")


def test_without_cookie_writes_a_deleted_cookie() -> None:
    response = Response().without_cookie(Cookie("session", "abc"))

    assert "session=delete" in response.get_headers().get_header_line(HeaderName.SET_COOKIE)


def test_send_writes_the_line_the_headers_and_the_body(capsys: Any) -> None:
    response = Response(
        body=make_body("hello"),
        status_code=StatusCode.NOT_FOUND,
        headers=HeaderCollection(Header("Content-Type", "text/html")),
    )

    response.send()

    written = capsys.readouterr().out

    assert "HTTP/1.1 404 Not Found" in written
    assert "Content-Type: text/html" in written
    assert "hello" in written


def test_send_http_line_returns_the_response(capsys: Any) -> None:
    response = Response()

    assert response.send_http_line() is response
    assert response.send_headers() is response
    assert response.send_body() is response

    capsys.readouterr()
