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
from valkyrja.http.message.uri.uri import Uri


def test_a_new_uri_is_empty() -> None:
    uri = Uri()

    assert uri.get_scheme() is Scheme.EMPTY
    assert uri.get_host() == ""
    assert uri.get_port() == 0
    assert not uri.has_port()
    assert str(uri) == ""


def test_the_standard_port_of_a_scheme_reads_as_absent() -> None:
    # A uri leaves out the port that its scheme implies, so `get_port` answers zero.
    assert Uri(scheme=Scheme.HTTP, host="valkyrja.io").get_port() == 0
    assert Uri(scheme=Scheme.HTTPS, host="valkyrja.io").get_port() == 0


def test_a_uri_with_no_host_reads_its_port_as_absent() -> None:
    # No host means no authority, so a port stands for nothing.
    assert Uri(scheme=Scheme.HTTP, port=8080).get_port() == 0


def test_is_secure_reads_the_scheme() -> None:
    assert Uri(scheme=Scheme.HTTPS).is_secure()
    assert not Uri(scheme=Scheme.HTTP).is_secure()


def test_a_named_port_wins_over_the_scheme() -> None:
    assert Uri(scheme=Scheme.HTTP, host="valkyrja.io", port=8080).get_port() == 8080
    assert Uri(scheme=Scheme.HTTPS, host="valkyrja.io", port=Port.HTTP).get_port() == Port.HTTP


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


def test_with_user_info_drops_the_password_when_no_user_holds_it() -> None:
    uri = Uri(username="user", password="secret")  # nosec B106

    cleared = uri.with_user_info("")

    assert cleared.get_username() == ""
    assert cleared.get_password() == ""


def test_with_user_info_keeps_a_password_that_a_user_holds() -> None:
    changed = Uri().with_user_info("user", "secret")  # nosec B106

    assert changed.get_username() == "user"
    assert changed.get_password() == "secret"  # nosec B105


def test_the_host_reads_in_lower_case() -> None:
    assert Uri(host="VALKYRJA.IO").get_host() == "valkyrja.io"


def test_an_ip_literal_host_keeps_its_brackets() -> None:
    assert Uri(host="[::1]").get_host() == "[::1]"


def test_a_host_encodes_a_character_it_cannot_hold() -> None:
    assert UriFactory.get_filtered_host("valkyrja io") == "valkyrja%20io"


def test_a_path_encodes_a_character_it_cannot_hold() -> None:
    assert Uri(path="/a b").get_path() == "/a%20b"
    assert Uri(path="/a/b").get_path() == "/a/b"
    assert Uri(path="//a").get_path() == "/a"
    assert Uri(path="a b").get_path() == "a%20b"


def test_a_path_refuses_a_query_string_and_a_fragment() -> None:
    with pytest.raises(HttpUriInvalidPathException, match="must not contain a query string"):
        Uri(path="/a?b=c")

    with pytest.raises(HttpUriInvalidPathException, match="must not contain a URI fragment"):
        Uri(path="/a#b")


def test_a_query_drops_the_question_mark_and_encodes_the_rest() -> None:
    assert Uri(query="?a=b").get_query() == "a=b"
    assert Uri(query="a=b c").get_query() == "a=b%20c"


def test_a_query_refuses_a_fragment() -> None:
    with pytest.raises(HttpUriInvalidQueryException, match="must not contain a URI fragment"):
        Uri(query="a=b#c")


def test_a_fragment_drops_the_hash_and_encodes_the_rest() -> None:
    assert Uri(fragment="#top").get_fragment() == "top"
    assert Uri(fragment="a b").get_fragment() == "a%20b"


def test_an_encoded_triplet_keeps_its_meaning_in_upper_case() -> None:
    assert Uri(path="/a%2fb").get_path() == "/a%2Fb"
    assert Uri(path="/100%").get_path() == "/100%25"


def test_each_with_method_filters_what_it_takes() -> None:
    assert Uri().with_host("VALKYRJA.IO").get_host() == "valkyrja.io"
    assert Uri().with_path("/a b").get_path() == "/a%20b"
    assert Uri().with_query("?a=b c").get_query() == "a=b%20c"
    assert Uri().with_fragment("#a b").get_fragment() == "a%20b"


def test_from_string_reads_each_part_of_a_full_uri() -> None:
    uri = UriFactory.from_string("https://user:secret@valkyrja.io:8080/path?a=b#top")

    assert uri.get_scheme() is Scheme.HTTPS
    assert uri.get_username() == "user"
    assert uri.get_password() == "secret"  # nosec B105
    assert uri.get_host() == "valkyrja.io"
    assert uri.get_port() == 8080
    assert uri.get_path() == "/path"
    assert uri.get_query() == "a=b"
    assert uri.get_fragment() == "top"


def test_from_string_reads_a_path_alone() -> None:
    uri = UriFactory.from_string("/path")

    assert uri.get_scheme() is Scheme.EMPTY
    assert uri.get_path() == "/path"
    assert uri.get_host() == ""


def test_from_string_reads_an_authority_with_no_scheme() -> None:
    uri = UriFactory.from_string("valkyrja.io/path")

    assert uri.get_host() == "valkyrja.io"
    assert uri.get_path() == "/path"


def test_from_string_reads_an_empty_string() -> None:
    uri = UriFactory.from_string("")

    assert uri.get_scheme() is Scheme.EMPTY
    assert str(uri) == ""


def test_from_string_reports_a_uri_it_cannot_read() -> None:
    with pytest.raises(HttpUriInvalidFromStringException, match="Invalid uri"):
        UriFactory.from_string("https://valkyrja.io:notaport/path")


def test_the_scheme_filter_reads_each_scheme_the_component_knows() -> None:
    assert UriFactory.get_filtered_scheme("HTTP") is Scheme.HTTP
    assert UriFactory.get_filtered_scheme("https") is Scheme.HTTPS
    assert UriFactory.get_filtered_scheme("http://") is Scheme.HTTP
    assert UriFactory.get_filtered_scheme("") is Scheme.EMPTY


def test_the_scheme_filter_reports_a_scheme_it_does_not_know() -> None:
    # A uri that opens with another scheme reads as an authority, so the filter is
    # where an unknown scheme reports the failure.
    with pytest.raises(HttpUriInvalidSchemeException, match="must be one of http or https"):
        UriFactory.get_filtered_scheme("ftp")


def test_the_user_info_encodes_a_character_it_cannot_hold() -> None:
    # The colon separates the username from the password, so the colon stays.
    uri = Uri(username="a b", password="c d", host="valkyrja.io")  # nosec B106

    assert uri.get_user_info() == "a%20b:c%20d"
    assert uri.get_authority() == "a%20b:c%20d@valkyrja.io"


def test_the_user_info_of_a_user_with_no_password() -> None:
    assert Uri(username="user").get_user_info() == "user"


def test_an_ip_literal_host_keeps_its_brackets_beside_a_port() -> None:
    # RFC 3986 brackets an IP literal, so the colons of the address stay apart from
    # the one before the port.
    uri = Uri(scheme=Scheme.HTTPS, host="[::1]", port=8080)

    assert uri.get_host_port() == "[::1]:8080"
    assert uri.get_authority() == "[::1]:8080"
    assert uri.get_scheme_host_port() == "https://[::1]:8080"


def test_the_scheme_host_port_of_a_uri_with_no_host() -> None:
    # No host means no authority, so there is nothing for a scheme to sit in front of.
    assert Uri(scheme=Scheme.HTTPS, port=8080).get_scheme_host_port() == ""
    assert Uri(port=8080).get_scheme_host_port() == ""
