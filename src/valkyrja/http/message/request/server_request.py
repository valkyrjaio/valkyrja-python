#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.protocol_version import ProtocolVersion
from valkyrja.http.message.enum.request_method import RequestMethod
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.param.attribute_param_collection import AttributeParamCollection
from valkyrja.http.message.param.contract.attribute_param_collection_contract import (
    AttributeParamCollectionContract,
)
from valkyrja.http.message.param.contract.cookie_param_collection_contract import (
    CookieParamCollectionContract,
)
from valkyrja.http.message.param.contract.parsed_body_param_collection_contract import (
    ParsedBodyParamCollectionContract,
)
from valkyrja.http.message.param.contract.query_param_collection_contract import (
    QueryParamCollectionContract,
)
from valkyrja.http.message.param.contract.server_param_collection_contract import (
    ServerParamCollectionContract,
)
from valkyrja.http.message.param.cookie_param_collection import CookieParamCollection
from valkyrja.http.message.param.parsed_body_param_collection import ParsedBodyParamCollection
from valkyrja.http.message.param.query_param_collection import QueryParamCollection
from valkyrja.http.message.param.server_param_collection import ServerParamCollection
from valkyrja.http.message.request.contract.server_request_contract import ServerRequestContract
from valkyrja.http.message.request.request import Request
from valkyrja.http.message.stream.contract.stream_contract import StreamContract
from valkyrja.http.message.uri.contract.uri_contract import UriContract

XML_HTTP_REQUEST = "XMLHttpRequest"
"""What a script in the browser writes into the `X-Requested-With` header."""


class ServerRequest(Request, ServerRequestContract):
    """A request that a server gives the application."""

    def __init__(
        self,
        uri: UriContract | None = None,
        method: RequestMethod = RequestMethod.GET,
        body: StreamContract | None = None,
        headers: HeaderCollectionContract | None = None,
        protocol_version: ProtocolVersion = ProtocolVersion.V1_1,
        server: ServerParamCollectionContract | None = None,
        cookies: CookieParamCollectionContract | None = None,
        query: QueryParamCollectionContract | None = None,
        parsed_body: ParsedBodyParamCollectionContract | None = None,
        attributes: AttributeParamCollectionContract | None = None,
    ) -> None:
        super().__init__(uri, method, body, headers, protocol_version)

        self._server: ServerParamCollectionContract = server if server is not None else ServerParamCollection()
        self._cookies: CookieParamCollectionContract = cookies if cookies is not None else CookieParamCollection()
        self._query: QueryParamCollectionContract = query if query is not None else QueryParamCollection()
        self._parsed_body: ParsedBodyParamCollectionContract = (
            parsed_body if parsed_body is not None else ParsedBodyParamCollection()
        )
        self._attributes: AttributeParamCollectionContract = (
            attributes if attributes is not None else AttributeParamCollection()
        )

    @override
    def get_server_params(self) -> ServerParamCollectionContract:
        return self._server

    @override
    def with_server_params(self, server: ServerParamCollectionContract) -> Self:
        new = copy(self)
        new._server = server

        return new

    @override
    def get_cookie_params(self) -> CookieParamCollectionContract:
        return self._cookies

    @override
    def with_cookie_params(self, cookies: CookieParamCollectionContract) -> Self:
        new = copy(self)
        new._cookies = cookies

        return new

    @override
    def get_query_params(self) -> QueryParamCollectionContract:
        return self._query

    @override
    def with_query_params(self, query: QueryParamCollectionContract) -> Self:
        new = copy(self)
        new._query = query

        return new

    @override
    def get_parsed_body(self) -> ParsedBodyParamCollectionContract:
        return self._parsed_body

    @override
    def with_parsed_body(self, params: ParsedBodyParamCollectionContract) -> Self:
        new = copy(self)
        new._parsed_body = params

        return new

    @override
    def get_attributes(self) -> AttributeParamCollectionContract:
        return self._attributes

    @override
    def with_attributes(self, attributes: AttributeParamCollectionContract) -> Self:
        new = copy(self)
        new._attributes = attributes

        return new

    @override
    def is_xml_http_request(self) -> bool:
        return self._headers.get_header_line(HeaderName.X_REQUESTED_WITH) == XML_HTTP_REQUEST
