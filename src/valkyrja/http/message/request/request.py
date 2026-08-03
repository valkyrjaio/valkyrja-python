#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.abstract.message import Message
from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.protocol_version import ProtocolVersion
from valkyrja.http.message.enum.request_method import RequestMethod
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.request.contract.request_contract import RequestContract
from valkyrja.http.message.stream.contract.stream_contract import StreamContract
from valkyrja.http.message.uri.contract.uri_contract import UriContract
from valkyrja.http.message.uri.uri import Uri


class Request(Message, RequestContract):
    """A request that the application answers."""

    def __init__(
        self,
        uri: UriContract | None = None,
        method: RequestMethod = RequestMethod.GET,
        body: StreamContract | None = None,
        headers: HeaderCollectionContract | None = None,
        protocol_version: ProtocolVersion = ProtocolVersion.V1_1,
    ) -> None:
        super().__init__(body, headers, protocol_version)

        self._uri: UriContract = uri if uri is not None else Uri()
        self._method = method
        self._request_target: str | None = None

        self._add_host_header_from_uri()

    @override
    def get_request_target(self) -> str:
        if self._request_target is not None:
            return self._request_target

        target = self._uri.get_path()
        query = self._uri.get_query()

        if query != "":
            target = f"{target}?{query}"

        return target if target != "" else "/"

    @override
    def with_request_target(self, request_target: str) -> Self:
        new = copy(self)
        new._request_target = request_target

        return new

    @override
    def get_method(self) -> RequestMethod:
        return self._method

    @override
    def with_method(self, method: RequestMethod) -> Self:
        new = copy(self)
        new._method = method

        return new

    @override
    def get_uri(self) -> UriContract:
        return self._uri

    @override
    def with_uri(self, uri: UriContract, preserve_host: bool = False) -> Self:
        new = copy(self)
        new._uri = uri

        if preserve_host and self._headers.has(HeaderName.HOST):
            return new

        if uri.get_host() == "":
            return new

        new._headers = self._headers.with_header(Header(HeaderName.HOST, new._get_host_from_uri()))

        return new

    def _get_host_from_uri(self) -> str:
        """Get the host of the uri, with the port after it."""
        host = self._uri.get_host()
        port = self._uri.get_port()

        return f"{host}:{port}" if port != 0 else host

    def _add_host_header_from_uri(self) -> None:
        """Add the host header, unless the caller gave one already."""
        if not self._headers.has(HeaderName.HOST) and self._uri.get_host() != "":
            self._headers = self._headers.with_header(Header(HeaderName.HOST, self._get_host_from_uri()))
