#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import TYPE_CHECKING, final

from valkyrja.http.message.uri.constant.port import Port
from valkyrja.http.message.uri.enum.scheme import Scheme
from valkyrja.http.message.uri.throwable.exception.http_uri_invalid_port_exception import (
    HttpUriInvalidPortException,
)

if TYPE_CHECKING:
    from valkyrja.http.message.uri.contract.uri_contract import UriContract


@final
class UriFactory:
    """Builds the parts of a uri, and the whole string."""

    @staticmethod
    def validate_port(port: int) -> None:
        """Report a port that TCP and UDP do not allow."""
        if not Port.is_valid(port):
            raise HttpUriInvalidPortException(f"Invalid port `{port}` specified; must be a valid TCP/UDP port")

    @staticmethod
    def is_standard_unsecure_port(scheme: Scheme, port: int) -> bool:
        """Get whether the port is the one that http uses."""
        return scheme is Scheme.HTTP and port == Port.HTTP

    @staticmethod
    def is_standard_secure_port(scheme: Scheme, port: int) -> bool:
        """Get whether the port is the one that https uses."""
        return scheme is Scheme.HTTPS and port == Port.HTTPS

    @staticmethod
    def is_standard_port(scheme: Scheme, host: str, port: int) -> bool:
        """Get whether the uri can leave the port out."""
        if scheme is Scheme.EMPTY:
            return host != "" and port <= 0

        if host == "" or port <= 0:
            return True

        return UriFactory.is_standard_unsecure_port(scheme, port) or UriFactory.is_standard_secure_port(scheme, port)

    @staticmethod
    def get_scheme_string_part(uri: UriContract) -> str:
        """Get the scheme, with the colon after it."""
        scheme = uri.get_scheme()

        return f"{scheme.value}:" if scheme is not Scheme.EMPTY else ""

    @staticmethod
    def get_authority_string_part(uri: UriContract) -> str:
        """Get the authority, with the two slashes before it."""
        authority = uri.get_authority()

        return f"//{authority}" if authority != "" else ""

    @staticmethod
    def get_path_string_part(uri: UriContract) -> str:
        """Get the path, with one slash in front of it."""
        path = uri.get_path()

        if path == "":
            return ""

        return path if path.startswith("/") else f"/{path}"

    @staticmethod
    def get_query_string_part(uri: UriContract) -> str:
        """Get the query string, with the question mark before it."""
        query = uri.get_query()

        return f"?{query}" if query != "" else ""

    @staticmethod
    def get_fragment_string_part(uri: UriContract) -> str:
        """Get the fragment, with the hash before it."""
        fragment = uri.get_fragment()

        return f"#{fragment}" if fragment != "" else ""

    @staticmethod
    def to_string(uri: UriContract) -> str:
        """Get the whole uri as a string."""
        return (
            UriFactory.get_scheme_string_part(uri)
            + UriFactory.get_authority_string_part(uri)
            + UriFactory.get_path_string_part(uri)
            + UriFactory.get_query_string_part(uri)
            + UriFactory.get_fragment_string_part(uri)
        )
