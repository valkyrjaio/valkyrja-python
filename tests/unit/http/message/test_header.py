#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Header, its values, and the collection."""

import pytest

from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.header.value.component.component import Component
from valkyrja.http.message.header.value.value import Value


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
    with pytest.raises(KeyError):
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
