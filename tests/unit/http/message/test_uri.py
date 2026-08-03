#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Uri."""

import pytest

from valkyrja.http.message.uri.constant.port import MAX_PORT, MIN_PORT, Port
from valkyrja.http.message.uri.enum.scheme import Scheme
from valkyrja.http.message.uri.factory.uri_factory import UriFactory
from valkyrja.http.message.uri.throwable.exception.http_uri_invalid_port_exception import (
    HttpUriInvalidPortException,
)
from valkyrja.http.message.uri.uri import Uri


def test_a_new_uri_is_empty() -> None:
    uri = Uri()

    assert uri.get_scheme() is Scheme.EMPTY
    assert uri.get_host() == ""
    assert uri.get_port() == 0
    assert not uri.has_port()
    assert str(uri) == ""


def test_a_scheme_gives_its_own_port() -> None:
    assert Uri(scheme=Scheme.HTTP).get_port() == Port.HTTP
    assert Uri(scheme=Scheme.HTTPS).get_port() == Port.HTTPS


def test_is_secure_reads_the_scheme() -> None:
    assert Uri(scheme=Scheme.HTTPS).is_secure()
    assert not Uri(scheme=Scheme.HTTP).is_secure()


def test_a_named_port_wins_over_the_scheme() -> None:
    assert Uri(scheme=Scheme.HTTP, port=8080).get_port() == 8080


def test_an_invalid_port_reports_a_failure() -> None:
    with pytest.raises(HttpUriInvalidPortException, match="Invalid port"):
        Uri(port=MAX_PORT + 1)


def test_with_port_reports_an_invalid_port() -> None:
    with pytest.raises(HttpUriInvalidPortException):
        Uri().with_port(0)


def test_the_port_bounds() -> None:
    assert Port.is_valid(MIN_PORT)
    assert Port.is_valid(MAX_PORT)
    assert not Port.is_valid(0)
    assert not Port.is_valid(MAX_PORT + 1)


def test_the_user_info_joins_the_name_and_the_password() -> None:
    assert Uri(username="user", password="secret").get_user_info() == "user:secret"


def test_the_user_info_is_the_name_alone_without_a_password() -> None:
    assert Uri(username="user").get_user_info() == "user"


def test_the_authority_is_empty_without_a_host() -> None:
    assert Uri(username="user").get_authority() == ""


def test_the_authority_holds_the_host() -> None:
    assert Uri(scheme=Scheme.HTTP, host="valkyrja.io").get_authority() == "valkyrja.io"


def test_the_authority_holds_the_user_info() -> None:
    uri = Uri(scheme=Scheme.HTTP, username="user", host="valkyrja.io")

    assert uri.get_authority() == "user@valkyrja.io"


def test_the_authority_leaves_out_a_standard_port() -> None:
    assert "80" not in Uri(scheme=Scheme.HTTP, host="valkyrja.io", port=80).get_authority()
    assert "443" not in Uri(scheme=Scheme.HTTPS, host="valkyrja.io", port=443).get_authority()


def test_the_authority_holds_a_port_that_is_not_standard() -> None:
    uri = Uri(scheme=Scheme.HTTP, host="valkyrja.io", port=8080)

    assert uri.get_authority() == "valkyrja.io:8080"


def test_the_authority_holds_a_port_without_a_scheme() -> None:
    assert Uri(host="valkyrja.io", port=8080).get_authority() == "valkyrja.io:8080"


def test_the_host_port() -> None:
    assert Uri(host="valkyrja.io", port=8080).get_host_port() == "valkyrja.io:8080"
    assert Uri(host="valkyrja.io").get_host_port() == "valkyrja.io"
    assert Uri(port=8080).get_host_port() == ""


def test_the_scheme_host_port() -> None:
    uri = Uri(scheme=Scheme.HTTPS, host="valkyrja.io")

    assert uri.get_scheme_host_port() == "https://valkyrja.io:443"
    assert Uri(host="valkyrja.io", port=8080).get_scheme_host_port() == "valkyrja.io:8080"


def test_the_string_holds_every_part() -> None:
    uri = Uri(
        scheme=Scheme.HTTPS,
        username="user",
        password="secret",  # nosec B106 — a test value, not a secret.
        host="valkyrja.io",
        port=8080,
        path="path",
        query="key=value",
        fragment="top",
    )

    assert str(uri) == "https://user:secret@valkyrja.io:8080/path?key=value#top"


def test_the_string_puts_a_slash_in_front_of_the_path() -> None:
    assert str(Uri(host="valkyrja.io", path="path")) == "//valkyrja.io/path"
    assert str(Uri(host="valkyrja.io", path="/path")) == "//valkyrja.io/path"


def test_the_string_leaves_out_an_empty_part() -> None:
    assert str(Uri(path="/path")) == "/path"
    assert str(Uri(query="key=value")) == "?key=value"
    assert str(Uri(fragment="top")) == "#top"


def test_every_setter_returns_a_copy() -> None:
    uri = Uri(scheme=Scheme.HTTP, host="valkyrja.io")

    assert uri.with_scheme(Scheme.HTTPS).get_scheme() is Scheme.HTTPS
    assert uri.with_username("user").get_username() == "user"
    assert uri.with_password("secret").get_password() == "secret"  # nosec B105
    assert uri.with_user_info("user", "secret").get_user_info() == "user:secret"
    assert uri.with_host("other.io").get_host() == "other.io"
    assert uri.with_port(8080).get_port() == 8080
    assert uri.with_path("/path").get_path() == "/path"
    assert uri.with_query("key=value").get_query() == "key=value"
    assert uri.with_fragment("top").get_fragment() == "top"

    assert uri.get_scheme() is Scheme.HTTP
    assert uri.get_host() == "valkyrja.io"
    assert uri.get_username() == ""


def test_a_scheme_with_no_host_leaves_the_port_out() -> None:
    """`Uri` answers early for an empty host, so the factory is tested directly."""
    assert UriFactory.is_standard_port(Scheme.HTTP, "", 80)


def test_a_scheme_with_no_port_leaves_the_port_out() -> None:
    assert UriFactory.is_standard_port(Scheme.HTTP, "valkyrja.io", 0)


def test_an_empty_scheme_leaves_the_port_out_only_with_a_host() -> None:
    assert UriFactory.is_standard_port(Scheme.EMPTY, "valkyrja.io", 0)
    assert not UriFactory.is_standard_port(Scheme.EMPTY, "", 0)
    assert not UriFactory.is_standard_port(Scheme.EMPTY, "valkyrja.io", 8080)


def test_a_port_that_is_not_standard_stays_in() -> None:
    assert not UriFactory.is_standard_port(Scheme.HTTP, "valkyrja.io", 8080)
    assert not UriFactory.is_standard_port(Scheme.HTTPS, "valkyrja.io", 80)
