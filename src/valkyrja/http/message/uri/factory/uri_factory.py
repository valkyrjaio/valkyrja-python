#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import re
from typing import TYPE_CHECKING, final
from urllib.parse import quote, urlsplit

from valkyrja.http.message.uri.constant.char import Char
from valkyrja.http.message.uri.constant.port import Port
from valkyrja.http.message.uri.enum.scheme import Scheme
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

if TYPE_CHECKING:
    from valkyrja.http.message.uri.contract.uri_contract import UriContract


@final
class UriFactory:
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
    def get_filtered_user_info(user_info: str) -> str:
        """Get the user info with each character it cannot hold encoded.

        A colon stands between the username and the password, so the colon stays.
        """
        return UriFactory._get_encoded(user_info, Char.USER_INFO)

    @staticmethod
    def get_filtered_host(host: str) -> str:
        """Get the host in lower case, with each character it cannot hold encoded.

        An IP literal sits in brackets and holds characters a reg-name forbids, so
        the brackets keep it as it is.
        """
        host = host.lower()

        if host.startswith("[") and host.endswith("]"):
            return host

        return UriFactory._get_encoded(host, Char.HOST)

    @staticmethod
    def validate_path(path: str) -> None:
        """Report a path that holds a query string or a fragment."""
        if "?" in path:
            raise HttpUriInvalidPathException(f"Invalid path of `{path}` provided; must not contain a query string")

        if "#" in path:
            raise HttpUriInvalidPathException(f"Invalid path of `{path}` provided; must not contain a URI fragment")

    @staticmethod
    def get_filtered_path(path: str) -> str:
        """Get the path with each character it cannot hold encoded."""
        UriFactory.validate_path(path)

        path = UriFactory._get_encoded(path, Char.PATH)

        if path.startswith("/"):
            return "/" + path.lstrip("/")

        return path

    @staticmethod
    def validate_query(query: str) -> None:
        """Report a query string that holds a fragment."""
        if "#" in query:
            raise HttpUriInvalidQueryException(
                f"Invalid query string of `{query}` provided; must not contain a URI fragment"
            )

    @staticmethod
    def get_filtered_query(query: str) -> str:
        """Get the query string with each character it cannot hold encoded."""
        UriFactory.validate_query(query)

        return UriFactory._get_encoded(query.lstrip("?"), Char.QUERY)

    @staticmethod
    def get_filtered_fragment(fragment: str) -> str:
        """Get the fragment with each character it cannot hold encoded."""
        return UriFactory._get_encoded(fragment.lstrip("#"), Char.QUERY)

    @staticmethod
    def from_string(uri: str) -> UriContract:
        """Build a uri from one string.

        A string that names no scheme and opens with no slash is an authority, so
        the two slashes go in front of it for the parse to read a host.
        """
        if (
            uri != ""
            and not uri.startswith("/")
            and not uri.startswith(Scheme.HTTP.value)
            and not uri.startswith(Scheme.HTTPS.value)
        ):
            uri = f"//{uri}"

        try:
            parts = urlsplit(uri)
            port = parts.port
        except ValueError as exception:
            raise HttpUriInvalidFromStringException(f"Invalid uri `{uri}` provided") from exception

        from valkyrja.http.message.uri.uri import Uri

        return Uri(
            scheme=UriFactory.get_filtered_scheme(parts.scheme),
            username=parts.username or "",
            password=parts.password or "",
            host=parts.hostname or "",
            port=port or 0,
            path=parts.path,
            query=parts.query,
            fragment=parts.fragment,
        )

    @staticmethod
    def get_filtered_scheme(scheme: str) -> Scheme:
        """Get the scheme member that one string names."""
        scheme = scheme.lower().rstrip(":/")

        if scheme == "":
            return Scheme.EMPTY

        try:
            return Scheme(scheme)
        except ValueError as exception:
            raise HttpUriInvalidSchemeException(
                f"Invalid scheme `{scheme}` provided; must be one of http or https"
            ) from exception

    @staticmethod
    def _get_encoded(value: str, allowed: str) -> str:
        """Get the value with each character outside the allowed set encoded.

        A percent-encoded triplet that is already there keeps its meaning, and its
        digits become upper case. Every other percent sign is a literal one.
        """
        pattern = re.compile(f"(%[A-Fa-f0-9]{{2}})|[^{allowed}]+")

        def replace(match: re.Match[str]) -> str:
            triplet = match.group(1)

            if triplet is not None:
                return triplet.upper()

            return quote(match.group(0), safe="")

        return pattern.sub(replace, value)

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
