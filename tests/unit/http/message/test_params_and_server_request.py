#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the parameter collections and the ServerRequest."""

from collections.abc import Callable
from typing import Any

import pytest

from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.request_method import RequestMethod
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.param.attribute_param_collection import AttributeParamCollection
from valkyrja.http.message.param.contract.param_collection_contract import ParamCollectionContract
from valkyrja.http.message.param.cookie_param_collection import CookieParamCollection
from valkyrja.http.message.param.param_collection import ParamCollection
from valkyrja.http.message.param.parsed_body_param_collection import ParsedBodyParamCollection
from valkyrja.http.message.param.parsed_json_param_collection import ParsedJsonParamCollection
from valkyrja.http.message.param.query_param_collection import QueryParamCollection
from valkyrja.http.message.param.server_param_collection import ServerParamCollection
from valkyrja.http.message.request.server_request import XML_HTTP_REQUEST, ServerRequest
from valkyrja.http.message.uri.uri import Uri

COLLECTIONS: list[Callable[[dict[str | int, Any]], ParamCollectionContract]] = [
    ParamCollection,
    ServerParamCollection,
    CookieParamCollection,
    QueryParamCollection,
    ParsedBodyParamCollection,
    ParsedJsonParamCollection,
    AttributeParamCollection,
]


def test_a_new_collection_is_empty() -> None:
    assert ParamCollection().get_all() == {}


def test_a_collection_holds_what_it_takes() -> None:
    params = ParamCollection({"page": 2, "sort": "name"})

    assert params.has("page")
    assert not params.has("missing")
    assert params.get("page") == 2
    assert params.get("missing") is None
    assert params.get_all() == {"page": 2, "sort": "name"}


def test_get_all_copies_the_parameters() -> None:
    params = ParamCollection({"page": 2})

    params.get_all().clear()

    assert params.get_all() == {"page": 2}


def test_get_only_and_get_all_except() -> None:
    params = ParamCollection({"page": 2, "sort": "name", "filter": "all"})

    assert params.get_only("page", "sort") == {"page": 2, "sort": "name"}
    assert params.get_all_except("page") == {"sort": "name", "filter": "all"}


def test_a_collection_takes_an_integer_key() -> None:
    params = ParamCollection({0: "first"})

    assert params.has(0)
    assert params.get_only(0) == {0: "first"}


def test_with_replaces_and_with_added_merges() -> None:
    params = ParamCollection({"page": 2})

    assert params.with_({"sort": "name"}).get_all() == {"sort": "name"}
    assert params.with_added({"sort": "name"}).get_all() == {"page": 2, "sort": "name"}
    assert params.get_all() == {"page": 2}


@pytest.mark.parametrize("collection", COLLECTIONS)
def test_every_collection_implements_the_contract(
    collection: Callable[[dict[str | int, Any]], ParamCollectionContract],
) -> None:
    built = collection({"key": "value"})

    assert isinstance(built, ParamCollectionContract)
    assert built.get("key") == "value"


def test_a_new_server_request_has_empty_collections() -> None:
    request = ServerRequest()

    assert request.get_server_params().get_all() == {}
    assert request.get_cookie_params().get_all() == {}
    assert request.get_query_params().get_all() == {}
    assert request.get_parsed_body().get_all() == {}
    assert request.get_attributes().get_all() == {}


def test_a_server_request_is_a_request() -> None:
    request = ServerRequest(uri=Uri(path="/users"), method=RequestMethod.POST)

    assert request.get_method() is RequestMethod.POST
    assert request.get_request_target() == "/users"


def test_a_server_request_holds_what_it_takes() -> None:
    request = ServerRequest(
        server=ServerParamCollection({"REQUEST_METHOD": "POST"}),
        cookies=CookieParamCollection({"session": "abc"}),
        query=QueryParamCollection({"page": 2}),
        parsed_body=ParsedBodyParamCollection({"name": "value"}),
        attributes=AttributeParamCollection({"user": 1}),
    )

    assert request.get_server_params().get("REQUEST_METHOD") == "POST"
    assert request.get_cookie_params().get("session") == "abc"
    assert request.get_query_params().get("page") == 2
    assert request.get_parsed_body().get("name") == "value"
    assert request.get_attributes().get("user") == 1


def test_every_setter_returns_a_copy() -> None:
    request = ServerRequest()

    assert request.with_server_params(ServerParamCollection({"a": 1})).get_server_params().get("a") == 1
    assert request.with_cookie_params(CookieParamCollection({"a": 1})).get_cookie_params().get("a") == 1
    assert request.with_query_params(QueryParamCollection({"a": 1})).get_query_params().get("a") == 1
    assert request.with_parsed_body(ParsedBodyParamCollection({"a": 1})).get_parsed_body().get("a") == 1
    assert request.with_attributes(AttributeParamCollection({"a": 1})).get_attributes().get("a") == 1

    assert request.get_server_params().get_all() == {}


def test_a_request_from_a_script_in_the_browser() -> None:
    request = ServerRequest(headers=HeaderCollection(Header(HeaderName.X_REQUESTED_WITH, XML_HTTP_REQUEST)))

    assert request.is_xml_http_request()


def test_a_request_that_no_script_made() -> None:
    assert not ServerRequest().is_xml_http_request()
