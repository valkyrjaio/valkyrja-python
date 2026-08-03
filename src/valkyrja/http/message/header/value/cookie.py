#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import time
from copy import copy
from datetime import UTC, datetime
from typing import Self, override
from urllib.parse import quote

from valkyrja.http.message.enum.same_site import SameSite
from valkyrja.http.message.header.value.component.component import Component
from valkyrja.http.message.header.value.component.contract.component_contract import (
    ComponentContract,
)
from valkyrja.http.message.header.value.contract.cookie_contract import CookieContract
from valkyrja.http.message.header.value.value import Value

ONE_YEAR_AND_A_SECOND = 31536001
"""How far into the past a deleted cookie expires."""

COOKIE_DATE_FORMAT = "%a, %d-%b-%Y %H:%M:%S GMT"
"""The date format that a cookie carries, which PHP spells `DateTimeInterface::COOKIE`."""


class Cookie(Value, CookieContract):
    """A cookie that a response sets."""

    def __init__(
        self,
        name: str,
        value: str = "",
        expire: int = 0,
        path: str = "/",
        domain: str = "",
        secure: bool = False,
        http_only: bool = True,
        raw: bool = False,
        same_site: SameSite = SameSite.LAX,
        delete: bool = False,
    ) -> None:
        super().__init__()

        self._name = name
        self._value = value
        self._expire = expire
        self._path = path
        self._domain = domain
        self._secure = secure
        self._http_only = http_only
        self._raw = raw
        self._same_site = same_site
        self._delete = delete

    @override
    def __str__(self) -> str:
        value = self._value
        expire = self._expire
        max_age = self.get_max_age()

        if self._delete:
            expire = int(time.time()) - ONE_YEAR_AND_A_SECOND
            max_age = -ONE_YEAR_AND_A_SECOND
            value = "delete"

        components: list[ComponentContract] = [Component(quote(self._name), quote(value))]

        if expire != 0:
            components.append(Component("expires", self._format_expire(expire)))
            components.append(Component("max-age", str(max_age)))

        components.append(Component("path", self._path))
        components.extend(self._get_flag_components())
        components.append(Component("samesite", self._same_site.value))

        return "; ".join(str(component) for component in components)

    @override
    def delete(self) -> Self:
        new = copy(self)
        new._delete = True

        return new

    @override
    def get_max_age(self) -> int:
        return self._expire - int(time.time()) if self._expire > 0 else 0

    @override
    def get_name(self) -> str:
        return self._name

    @override
    def with_name(self, name: str) -> Self:
        new = copy(self)
        new._name = name

        return new

    @override
    def get_value(self) -> str:
        return self._value

    @override
    def with_value(self, value: str) -> Self:
        new = copy(self)
        new._value = value

        return new

    @override
    def get_expire(self) -> int:
        return self._expire

    @override
    def with_expire(self, expire: int) -> Self:
        new = copy(self)
        new._expire = expire

        return new

    @override
    def get_path(self) -> str:
        return self._path

    @override
    def with_path(self, path: str) -> Self:
        new = copy(self)
        new._path = path

        return new

    @override
    def get_domain(self) -> str:
        return self._domain

    @override
    def with_domain(self, domain: str) -> Self:
        new = copy(self)
        new._domain = domain

        return new

    @override
    def is_secure(self) -> bool:
        return self._secure

    @override
    def with_secure(self, secure: bool) -> Self:
        new = copy(self)
        new._secure = secure

        return new

    @override
    def is_http_only(self) -> bool:
        return self._http_only

    @override
    def with_http_only(self, http_only: bool = False) -> Self:
        new = copy(self)
        new._http_only = http_only

        return new

    @override
    def is_raw(self) -> bool:
        return self._raw

    @override
    def with_raw(self, raw: bool) -> Self:
        new = copy(self)
        new._raw = raw

        return new

    @override
    def get_same_site(self) -> SameSite:
        return self._same_site

    @override
    def with_same_site(self, same_site: SameSite) -> Self:
        new = copy(self)
        new._same_site = same_site

        return new

    def _get_flag_components(self) -> list[ComponentContract]:
        """Get a component for each flag that the cookie sets."""
        components: list[ComponentContract] = []

        if self._domain != "":
            components.append(Component("domain", self._domain))

        if self._secure:
            components.append(Component("secure"))

        if self._http_only:
            components.append(Component("httponly"))

        return components

    @staticmethod
    def _format_expire(expire: int) -> str:
        """Get the time that a cookie expires at, in the format a cookie carries."""
        return datetime.fromtimestamp(expire, tz=UTC).strftime(COOKIE_DATE_FORMAT)
