#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self

from valkyrja.http.message.enum.same_site import SameSite
from valkyrja.http.message.header.value.contract.value_contract import ValueContract


class CookieContract(ValueContract):
    """The contract for a cookie that a response sets."""

    @abstractmethod
    def delete(self) -> Self:
        """Get a copy of the cookie that tells the browser to drop it."""

    @abstractmethod
    def get_max_age(self) -> int:
        """Get how many seconds the cookie lives for."""

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the cookie."""

    @abstractmethod
    def with_name(self, name: str) -> Self:
        """Get a copy of the cookie that carries a different name."""

    @abstractmethod
    def get_value(self) -> str:
        """Get the value of the cookie."""

    @abstractmethod
    def with_value(self, value: str) -> Self:
        """Get a copy of the cookie that carries a different value."""

    @abstractmethod
    def get_expire(self) -> int:
        """Get the time that the cookie expires at."""

    @abstractmethod
    def with_expire(self, expire: int) -> Self:
        """Get a copy of the cookie that expires at a different time."""

    @abstractmethod
    def get_path(self) -> str:
        """Get the path that the cookie applies to."""

    @abstractmethod
    def with_path(self, path: str) -> Self:
        """Get a copy of the cookie that applies to a different path."""

    @abstractmethod
    def get_domain(self) -> str:
        """Get the domain that the cookie applies to."""

    @abstractmethod
    def with_domain(self, domain: str) -> Self:
        """Get a copy of the cookie that applies to a different domain."""

    @abstractmethod
    def is_secure(self) -> bool:
        """Get whether the browser sends the cookie over https alone."""

    @abstractmethod
    def with_secure(self, secure: bool) -> Self:
        """Get a copy of the cookie that changes the secure flag."""

    @abstractmethod
    def is_http_only(self) -> bool:
        """Get whether the cookie is hidden from a script in the browser."""

    @abstractmethod
    def with_http_only(self, http_only: bool = False) -> Self:
        """Get a copy of the cookie that changes the http-only flag."""

    @abstractmethod
    def is_raw(self) -> bool:
        """Get whether the response writes the value without escaping it."""

    @abstractmethod
    def with_raw(self, raw: bool) -> Self:
        """Get a copy of the cookie that changes the raw flag."""

    @abstractmethod
    def get_same_site(self) -> SameSite:
        """Get when the browser sends the cookie from another site."""

    @abstractmethod
    def with_same_site(self, same_site: SameSite) -> Self:
        """Get a copy of the cookie that carries a different same-site value."""
