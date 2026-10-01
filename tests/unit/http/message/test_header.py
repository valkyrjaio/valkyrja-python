#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Header, its values, and the collection."""

import pytest

from valkyrja.http.message.constant.header_value import HeaderValue
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.factory.header_factory import HeaderFactory
from valkyrja.http.message.header.header import Header
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
from valkyrja.http.message.header.value.component.component import Component
from valkyrja.http.message.header.value.value import Value
from valkyrja.http.message.throwable.exception.abstract.http_message_invalid_argument_exception import (
    HttpMessageInvalidArgumentException,
)


def test_a_component_holds_a_token_and_a_text() -> None:
    component = Component("charset", "utf-8")

    assert component.get_token() == "charset"
    assert component.get_text() == "utf-8"
    assert str(component) == "charset=utf-8"


def test_a_component_with_no_text_is_the_token_alone() -> None:
    assert str(Component("gzip")) == "gzip"


def test_the_component_setters_return_copies() -> None:
    component = Component("charset", "utf-8")

    assert component.with_token("boundary").get_token() == "boundary"
    assert component.with_text("ascii").get_text() == "ascii"
    assert component.get_token() == "charset"


def test_a_component_reads_a_string() -> None:
    component = Component.from_string(" charset = utf-8 ")

    assert component.get_token() == "charset"
    assert component.get_text() == "utf-8"


def test_a_component_reads_a_string_with_no_text() -> None:
    component = Component.from_string("gzip")

    assert component.get_token() == "gzip"
    assert component.get_text() == ""


def test_a_value_joins_its_components() -> None:
    value = Value(Component("text/html"), Component("charset", "utf-8"))

    assert str(value) == "text/html; charset=utf-8"
    assert len(value.get_components()) == 2


def test_a_value_takes_a_string_component() -> None:
    assert str(Value("charset=utf-8")) == "charset=utf-8"


def test_the_value_setters_return_copies() -> None:
    value = Value(Component("text/html"))

    assert len(value.with_components(Component("a"), Component("b")).get_components()) == 2
    assert len(value.with_added_components(Component("b")).get_components()) == 2
    assert len(value.get_components()) == 1


def test_get_components_copies_the_list() -> None:
    value = Value(Component("text/html"))

    value.get_components().clear()

    assert len(value.get_components()) == 1


def test_a_value_reads_a_string() -> None:
    value = Value.from_string("text/html; charset=utf-8")

    assert [component.get_token() for component in value.get_components()] == [
        "text/html",
        "charset",
    ]


def test_a_value_reads_a_string_with_an_empty_part() -> None:
    assert len(Value.from_string("text/html;;").get_components()) == 1


def test_a_header_holds_its_name_and_values() -> None:
    header = Header("Content-Type", "text/html")

    assert header.get_name() == "Content-Type"
    assert header.get_normalized_name() == "content-type"
    assert header.get_header_line() == "text/html"
    assert str(header) == "Content-Type: text/html"


def test_a_header_joins_several_values_by_a_comma() -> None:
    header = Header("Accept", "text/html", "application/json")

    assert header.get_header_line() == "text/html, application/json"


def test_a_header_with_no_value_is_an_empty_string() -> None:
    assert str(Header("Content-Type")) == ""


def test_the_header_setters_return_copies() -> None:
    header = Header("Content-Type", "text/html")

    renamed = header.with_name("Accept")

    assert renamed.get_name() == "Accept"
    assert renamed.get_normalized_name() == "accept"
    assert header.get_name() == "Content-Type"

    assert header.with_values("application/json").get_header_line() == "application/json"
    assert len(header.with_added_values("application/json").get_values()) == 2
    assert len(header.get_values()) == 1


def test_get_values_copies_the_list() -> None:
    header = Header("Accept", "text/html")

    header.get_values().clear()

    assert len(header.get_values()) == 1


def test_a_header_takes_a_value_object() -> None:
    header = Header("Content-Type", Value(Component("text/html")))

    assert header.get_header_line() == "text/html"


def test_a_new_collection_is_empty() -> None:
    collection = HeaderCollection()

    assert collection.get_all() == []
    assert not collection.has("Content-Type")
    assert collection.get_header_line("Content-Type") == ""


def test_a_collection_reads_a_header_whatever_the_case() -> None:
    collection = HeaderCollection(Header("Content-Type", "text/html"))

    assert collection.has("content-type")
    assert collection.has("CONTENT-TYPE")
    assert collection.get("content-type").get_name() == "Content-Type"
    assert collection.get_header_line("CONTENT-TYPE") == "text/html"


def test_get_raises_for_a_header_that_the_collection_does_not_hold() -> None:
    # The component names the failure, rather than leaking the KeyError of a dict.
    with pytest.raises(HttpHeaderInvalidHeaderNameException, match="Content-Type does not exist"):
        HeaderCollection().get("Content-Type")


def test_get_only_answers_with_the_headers_that_the_caller_names() -> None:
    collection = HeaderCollection(Header("Content-Type", "text/html"), Header("Accept", "application/json"))

    only = collection.get_only("accept")

    assert [header.get_name() for header in only] == ["Accept"]


def test_get_all_except_leaves_out_the_headers_that_the_caller_names() -> None:
    collection = HeaderCollection(Header("Content-Type", "text/html"), Header("Accept", "application/json"))

    rest = collection.get_all_except("Accept")

    assert [header.get_name() for header in rest] == ["Content-Type"]


def test_with_header_returns_a_copy() -> None:
    collection = HeaderCollection()

    added = collection.with_header(Header("Accept", "text/html"))

    assert added.has("Accept")
    assert not collection.has("Accept")


def test_with_header_replaces_a_header_of_the_same_name() -> None:
    collection = HeaderCollection(Header("Accept", "text/html"))

    replaced = collection.with_header(Header("accept", "application/json"))

    assert len(replaced.get_all()) == 1
    assert replaced.get_header_line("Accept") == "application/json"


def test_without_header_returns_a_copy() -> None:
    collection = HeaderCollection(Header("Accept", "text/html"))

    removed = collection.without_header("ACCEPT")

    assert not removed.has("Accept")
    assert collection.has("Accept")


def test_without_header_accepts_a_name_the_collection_does_not_hold() -> None:
    collection = HeaderCollection().without_header("Accept")

    assert collection.get_all() == []


def test_a_header_name_takes_only_what_rfc_7230_allows() -> None:
    assert HeaderFactory.is_valid_name("Content-Type")
    assert HeaderFactory.is_valid_name("X-Custom_Header~1")
    assert not HeaderFactory.is_valid_name("")
    assert not HeaderFactory.is_valid_name("Content Type")
    assert not HeaderFactory.is_valid_name("Content:Type")
    assert not HeaderFactory.is_valid_name("Content\nType")


@pytest.mark.parametrize("name", ["", "Content Type", "Set-Cookie\r\nX-Injected: yes"])
def test_a_header_refuses_an_invalid_name(name: str) -> None:
    with pytest.raises(HttpHeaderInvalidNameException, match="is not valid header name"):
        Header(name, "value")


def test_with_name_refuses_an_invalid_name() -> None:
    with pytest.raises(HttpHeaderInvalidNameException):
        Header("Content-Type", "text/html").with_name("Bad Name")


def test_a_header_value_takes_only_what_rfc_7230_allows() -> None:
    assert HeaderFactory.is_valid_value("text/html")
    assert HeaderFactory.is_valid_value("one\r\n two")
    assert not HeaderFactory.is_valid_value("one\ntwo")
    assert not HeaderFactory.is_valid_value("one\rtwo")
    assert not HeaderFactory.is_valid_value("one\r\ntwo")
    assert not HeaderFactory.is_valid_value("one\x00two")


@pytest.mark.parametrize("value", ["text/html\r\nX-Injected: yes", "text/html\nX-Injected: yes", "a\x00b"])
def test_a_header_refuses_a_value_that_would_split_the_response(value: str) -> None:
    with pytest.raises(HttpHeaderInvalidValueException, match="is not valid header value"):
        Header("Content-Type", value)


def test_assert_valid_name_accepts_a_name_rfc_7230_allows() -> None:
    HeaderFactory.assert_valid_name("Content-Type")


def test_assert_valid_value_accepts_a_value_rfc_7230_allows() -> None:
    HeaderFactory.assert_valid_value("text/html")


def test_the_filter_drops_each_character_a_value_cannot_hold() -> None:
    assert HeaderFactory.get_filtered_value("text/html") == "text/html"
    assert HeaderFactory.get_filtered_value("one\x00two") == "onetwo"
    assert HeaderFactory.get_filtered_value("one\x7ftwo") == "onetwo"
    assert HeaderFactory.get_filtered_value("one\ttwo") == "one\ttwo"


def test_the_filter_keeps_a_fold_and_drops_a_bare_carriage_return() -> None:
    assert HeaderFactory.get_filtered_value("one\r\n two") == "one\r\n two"
    assert HeaderFactory.get_filtered_value("one\r\n\ttwo") == "one\r\n\ttwo"
    assert HeaderFactory.get_filtered_value("one\rtwo") == "onetwo"
    assert HeaderFactory.get_filtered_value("one\r\ntwo") == "onetwo"
    assert HeaderFactory.get_filtered_value("one\r") == "one"


def test_from_value_reads_the_name_and_each_value_of_one_line() -> None:
    header = Header.from_value("Content-Type:text/html")

    assert header.get_name() == "Content-Type"
    assert header.get_header_line() == "text/html"


def test_from_value_reads_several_values() -> None:
    header = Header.from_value("Accept:text/html,application/json")

    assert [str(value) for value in header.get_values()] == ["text/html", "application/json"]


def test_from_value_reads_a_line_that_carries_no_value() -> None:
    header = Header.from_value("Content-Type")

    assert header.get_name() == "Content-Type"
    assert header.get_values() == []


def test_a_header_answers_array_access_and_iteration() -> None:
    header = Header("Accept", "text/html", "application/json")

    assert str(header[0]) == "text/html"
    assert len(header) == 2
    assert [str(value) for value in header] == ["text/html", "application/json"]


def test_a_header_refuses_a_write_to_one_position() -> None:
    header = Header("Accept", "text/html")

    with pytest.raises(HttpHeaderUnsupportedOffsetSetException, match="with_values"):
        header[0] = "application/json"


def test_a_header_refuses_the_removal_of_one_position() -> None:
    header = Header("Accept", "text/html")

    with pytest.raises(HttpHeaderUnsupportedOffsetUnsetException, match="with_values"):
        del header[0]


def test_with_headers_holds_the_named_headers_alone() -> None:
    collection = HeaderCollection(Header("Content-Type", "text/html"))

    changed = collection.with_headers(Header("Accept", "application/json"))

    assert [header.get_name() for header in changed.get_all()] == ["Accept"]
    assert [header.get_name() for header in collection.get_all()] == ["Content-Type"]


def test_with_added_headers_keeps_the_headers_the_collection_holds() -> None:
    collection = HeaderCollection(Header("Content-Type", "text/html"))

    changed = collection.with_added_headers(Header("Accept", "application/json"))

    assert sorted(header.get_name() for header in changed.get_all()) == ["Accept", "Content-Type"]


def test_without_headers_drops_each_name_the_caller_gives() -> None:
    collection = HeaderCollection(
        Header("Content-Type", "text/html"), Header("Accept", "application/json"), Header("Host", "localhost")
    )

    changed = collection.without_headers("content-type", "ACCEPT")

    assert [header.get_name() for header in changed.get_all()] == ["Host"]
    assert len(collection.get_all()) == 3


def test_the_header_value_constant() -> None:
    assert HeaderValue.BEARER == "Bearer"


def test_the_invalid_header_param_exception_names_the_failure() -> None:
    exception = HttpHeaderInvalidHeaderParamException("Param must be header")

    assert str(exception) == "Param must be header"
    assert isinstance(exception, HttpMessageInvalidArgumentException)
