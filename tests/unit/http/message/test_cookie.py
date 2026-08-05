#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Cookie."""

import time

from valkyrja.http.message.enum.same_site import SameSite
from valkyrja.http.message.header.value.contract.value_contract import ValueContract
from valkyrja.http.message.header.value.cookie import ONE_YEAR_AND_A_SECOND, Cookie


def test_a_cookie_holds_its_defaults() -> None:
    cookie = Cookie("session")

    assert cookie.get_name() == "session"
    assert cookie.get_value() == ""
    assert cookie.get_expire() == 0
    assert cookie.get_path() == "/"
    assert cookie.get_domain() == ""
    assert not cookie.is_secure()
    assert cookie.is_http_only()
    assert not cookie.is_raw()
    assert cookie.get_same_site() is SameSite.LAX


def test_a_cookie_is_a_header_value() -> None:
    assert isinstance(Cookie("session"), ValueContract)


def test_a_cookie_writes_its_name_and_value() -> None:
    assert str(Cookie("session", "abc")).startswith("session=abc")


def test_a_cookie_escapes_its_name_and_value() -> None:
    assert "a%20b" in str(Cookie("a b", "c d"))


def test_a_cookie_writes_the_path_and_the_same_site() -> None:
    written = str(Cookie("session"))

    assert "path=/" in written
    assert "samesite=lax" in written


def test_a_cookie_writes_http_only_by_default() -> None:
    assert "httponly" in str(Cookie("session"))


def test_a_cookie_leaves_out_http_only_when_it_is_off() -> None:
    assert "httponly" not in str(Cookie("session", http_only=False))


def test_a_cookie_writes_secure_when_it_is_on() -> None:
    assert "secure" in str(Cookie("session", secure=True))
    assert "secure" not in str(Cookie("session"))


def test_a_cookie_writes_the_domain_when_it_has_one() -> None:
    assert "domain=valkyrja.io" in str(Cookie("session", domain="valkyrja.io"))
    assert "domain" not in str(Cookie("session"))


def test_a_cookie_with_no_expire_writes_no_expiry() -> None:
    written = str(Cookie("session"))

    assert "expires" not in written
    assert "max-age" not in written


def test_a_cookie_writes_its_expiry() -> None:
    expire = int(time.time()) + 3600
    written = str(Cookie("session", expire=expire))

    assert "expires=" in written
    assert "max-age=" in written
    assert "GMT" in written


def test_the_max_age_counts_from_now() -> None:
    cookie = Cookie("session", expire=int(time.time()) + 3600)

    assert 3590 <= cookie.get_max_age() <= 3600


def test_a_cookie_with_no_expire_has_no_max_age() -> None:
    assert Cookie("session").get_max_age() == 0


def test_delete_returns_a_copy_that_expires_in_the_past() -> None:
    cookie = Cookie("session", "abc")

    deleted = cookie.delete()

    assert deleted is not cookie
    assert "session=delete" in str(deleted)
    assert f"max-age=-{ONE_YEAR_AND_A_SECOND}" in str(deleted)
    assert "session=abc" in str(cookie)


def test_every_setter_returns_a_copy() -> None:
    cookie = Cookie("session")

    assert cookie.with_name("other").get_name() == "other"
    assert cookie.with_value("abc").get_value() == "abc"
    assert cookie.with_expire(10).get_expire() == 10
    assert cookie.with_path("/app").get_path() == "/app"
    assert cookie.with_domain("valkyrja.io").get_domain() == "valkyrja.io"
    assert cookie.with_secure(True).is_secure()
    assert not cookie.with_http_only().is_http_only()
    assert cookie.with_http_only(True).is_http_only()
    assert cookie.with_raw(True).is_raw()
    assert cookie.with_same_site(SameSite.STRICT).get_same_site() is SameSite.STRICT

    assert cookie.get_name() == "session"
    assert cookie.get_path() == "/"
    assert not cookie.is_secure()
