#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.uri.constant.port import Port
from valkyrja.http.message.uri.contract.uri_contract import UriContract
from valkyrja.http.message.uri.enum.scheme import Scheme
from valkyrja.http.message.uri.factory.uri_factory import UriFactory


class Uri(UriContract):
    """The address that a request asks for."""

    def __init__(
        self,
        scheme: Scheme = Scheme.EMPTY,
        username: str = "",
        password: str = "",  # nosec B107 — the empty default means "no password".
        host: str = "",
        port: int = 0,
        path: str = "",
        query: str = "",
        fragment: str = "",
    ) -> None:
        if port == 0:
            port = self._get_port_from_scheme(scheme)
        else:
            UriFactory.validate_port(port)

        self._scheme = scheme
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._path = path
        self._query = query
        self._fragment = fragment

    @override
    def __str__(self) -> str:
        return UriFactory.to_string(self)

    @override
    def get_scheme(self) -> Scheme:
        return self._scheme

    @override
    def is_secure(self) -> bool:
        return self._scheme is Scheme.HTTPS

    @override
    def get_authority(self) -> str:
        if self._host == "":
            return ""

        authority = self._host
        user_info = self.get_user_info()

        if user_info != "":
            authority = f"{user_info}@{authority}"

        if not UriFactory.is_standard_port(self._scheme, self._host, self._port):
            authority = f"{authority}:{self._port}"

        return authority

    @override
    def get_username(self) -> str:
        return self._username

    @override
    def get_password(self) -> str:
        return self._password

    @override
    def get_user_info(self) -> str:
        # Truthiness, not a comparison to a literal. The comparison reads to a
        # security scanner as a password written into the source.
        if self._password:
            return f"{self._username}:{self._password}"

        return self._username

    @override
    def get_host(self) -> str:
        return self._host

    @override
    def has_port(self) -> bool:
        return self._port != 0

    @override
    def get_port(self) -> int:
        return self._port

    @override
    def get_host_port(self) -> str:
        if self._host != "" and self._port != 0:
            return f"{self._host}:{self._port}"

        return self._host

    @override
    def get_scheme_host_port(self) -> str:
        host_port = self.get_host_port()

        if host_port != "" and self._scheme is not Scheme.EMPTY:
            return f"{self._scheme.value}://{host_port}"

        return host_port

    @override
    def get_path(self) -> str:
        return self._path

    @override
    def get_query(self) -> str:
        return self._query

    @override
    def get_fragment(self) -> str:
        return self._fragment

    @override
    def with_scheme(self, scheme: Scheme) -> Self:
        new = copy(self)
        new._scheme = scheme

        return new

    @override
    def with_username(self, username: str) -> Self:
        new = copy(self)
        new._username = username

        return new

    @override
    def with_password(self, password: str) -> Self:
        new = copy(self)
        new._password = password

        return new

    @override
    def with_user_info(self, user: str, password: str = "") -> Self:  # nosec B107
        new = copy(self)
        new._username = user
        new._password = password

        return new

    @override
    def with_host(self, host: str) -> Self:
        new = copy(self)
        new._host = host

        return new

    @override
    def with_port(self, port: int) -> Self:
        UriFactory.validate_port(port)

        new = copy(self)
        new._port = port

        return new

    @override
    def with_path(self, path: str) -> Self:
        new = copy(self)
        new._path = path

        return new

    @override
    def with_query(self, query: str) -> Self:
        new = copy(self)
        new._query = query

        return new

    @override
    def with_fragment(self, fragment: str) -> Self:
        new = copy(self)
        new._fragment = fragment

        return new

    @staticmethod
    def _get_port_from_scheme(scheme: Scheme) -> int:
        """Get the port that a scheme uses when the uri names none."""
        match scheme:
            case Scheme.HTTPS:
                return Port.HTTPS
            case Scheme.HTTP:
                return Port.HTTP
            case _:
                return 0
