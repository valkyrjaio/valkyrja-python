#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.http.message.uri.enum.scheme import Scheme


class UriContract(ABC):
    """The contract for the address that a request asks for."""

    @abstractmethod
    def __str__(self) -> str:
        """Get the whole uri as a string."""

    @abstractmethod
    def get_scheme(self) -> Scheme:
        """Get the scheme of the uri."""

    @abstractmethod
    def is_secure(self) -> bool:
        """Get whether the scheme is https."""

    @abstractmethod
    def get_authority(self) -> str:
        """Get the user information, the host, and the port."""

    @abstractmethod
    def get_username(self) -> str:
        """Get the user name of the uri."""

    @abstractmethod
    def get_password(self) -> str:
        """Get the password of the uri."""

    @abstractmethod
    def get_user_info(self) -> str:
        """Get the user name and the password."""

    @abstractmethod
    def get_host(self) -> str:
        """Get the host of the uri."""

    @abstractmethod
    def has_port(self) -> bool:
        """Get whether the uri carries a port."""

    @abstractmethod
    def get_port(self) -> int:
        """Get the port of the uri."""

    @abstractmethod
    def get_host_port(self) -> str:
        """Get the host and the port."""

    @abstractmethod
    def get_scheme_host_port(self) -> str:
        """Get the scheme, the host, and the port."""

    @abstractmethod
    def get_path(self) -> str:
        """Get the path of the uri."""

    @abstractmethod
    def get_query(self) -> str:
        """Get the query string of the uri."""

    @abstractmethod
    def get_fragment(self) -> str:
        """Get the fragment of the uri."""

    @abstractmethod
    def with_scheme(self, scheme: Scheme) -> Self:
        """Get a copy of the uri that carries a different scheme."""

    @abstractmethod
    def with_username(self, username: str) -> Self:
        """Get a copy of the uri that carries a different user name."""

    @abstractmethod
    def with_password(self, password: str) -> Self:
        """Get a copy of the uri that carries a different password."""

    @abstractmethod
    def with_user_info(  # nosec B107 — the empty default means "no password", not a secret.
        self, user: str, password: str = ""
    ) -> Self:
        """Get a copy of the uri that carries different user information.

        A uri carries no password in almost every case, so the empty default
        says that the uri has none.
        """

    @abstractmethod
    def with_host(self, host: str) -> Self:
        """Get a copy of the uri that carries a different host."""

    @abstractmethod
    def with_port(self, port: int) -> Self:
        """Get a copy of the uri that carries a different port."""

    @abstractmethod
    def with_path(self, path: str) -> Self:
        """Get a copy of the uri that carries a different path."""

    @abstractmethod
    def with_query(self, query: str) -> Self:
        """Get a copy of the uri that carries a different query string."""

    @abstractmethod
    def with_fragment(self, fragment: str) -> Self:
        """Get a copy of the uri that carries a different fragment."""
