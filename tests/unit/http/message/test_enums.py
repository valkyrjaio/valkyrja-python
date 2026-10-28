#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the enums of the Http Message subcomponent."""

import pytest

from valkyrja.http.message.constant.content_type_value import ContentTypeValue
from valkyrja.http.message.enum.protocol_version import ProtocolVersion
from valkyrja.http.message.enum.request_method import RequestMethod
from valkyrja.http.message.enum.same_site import SameSite
from valkyrja.http.message.enum.status_code import StatusCode


def test_every_request_method_names_itself() -> None:
    for method in RequestMethod:
        assert method.value == method.name


def test_the_request_methods_that_http_defines() -> None:
    assert RequestMethod.GET.value == "GET"
    assert RequestMethod.POST.value == "POST"
    assert RequestMethod.DELETE.value == "DELETE"
    assert RequestMethod.PATCH.value == "PATCH"


def test_any_is_a_route_method_and_not_a_request_method() -> None:
    assert RequestMethod.ANY.value == "ANY"


def test_the_protocol_versions() -> None:
    assert [version.value for version in ProtocolVersion] == ["1.0", "1.1", "2", "3"]


def test_the_same_site_values() -> None:
    assert [value.value for value in SameSite] == ["none", "lax", "strict"]


def test_a_status_code_is_an_integer() -> None:
    assert isinstance(StatusCode.OK, int)
    assert StatusCode.OK.value == 200


@pytest.mark.parametrize(
    ("code", "value"),
    [
        (StatusCode.CONTINUE, 100),
        (StatusCode.OK, 200),
        (StatusCode.MOVED_PERMANENTLY, 301),
        (StatusCode.NOT_FOUND, 404),
        (StatusCode.I_AM_A_TEAPOT, 418),
        (StatusCode.INTERNAL_SERVER_ERROR, 500),
        (StatusCode.NETWORK_AUTHENTICATION_REQUIRED, 511),
    ],
)
def test_each_status_code_carries_its_number(code: StatusCode, value: int) -> None:
    assert code.value == value


def test_every_status_code_is_in_a_class_that_http_defines() -> None:
    for code in StatusCode:
        assert 100 <= code.value <= 599


def test_each_status_code_is_unique() -> None:
    assert len({code.value for code in StatusCode}) == len(StatusCode)


def test_the_status_code_answers_its_number() -> None:
    assert StatusCode.OK.code() == 200
    assert StatusCode.NOT_FOUND.code() == 404


def test_the_status_code_reports_a_failure_of_the_server() -> None:
    assert StatusCode.INTERNAL_SERVER_ERROR.is_error()
    assert StatusCode.NETWORK_AUTHENTICATION_REQUIRED.is_error()
    assert not StatusCode.NOT_FOUND.is_error()
    assert not StatusCode.OK.is_error()


def test_the_request_methods_leave_out_the_routing_member() -> None:
    methods = RequestMethod.all()

    assert RequestMethod.ANY not in methods
    assert methods == [
        RequestMethod.GET,
        RequestMethod.HEAD,
        RequestMethod.POST,
        RequestMethod.PUT,
        RequestMethod.DELETE,
        RequestMethod.CONNECT,
        RequestMethod.OPTIONS,
        RequestMethod.TRACE,
        RequestMethod.PATCH,
    ]


def test_the_content_type_values() -> None:
    assert ContentTypeValue.APPLICATION_JAVASCRIPT == "application/javascript"
    assert ContentTypeValue.APPLICATION_XML == "application/xml"
    assert ContentTypeValue.APPLICATION_XML_UTF8 == "application/xml; charset=utf-8"
    assert ContentTypeValue.APPLICATION_X_WWW_FORM == "application/x-www-form-urlencoded"
    assert ContentTypeValue.MULTIPART_FORM_DATA == "multipart/form-data"
    assert ContentTypeValue.TEXT_JAVASCRIPT == "text/javascript"
