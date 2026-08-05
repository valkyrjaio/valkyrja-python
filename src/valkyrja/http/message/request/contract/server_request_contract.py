#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self

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
from valkyrja.http.message.request.contract.request_contract import RequestContract


class ServerRequestContract(RequestContract):
    """The contract for a request that a server gives the application."""

    @abstractmethod
    def get_server_params(self) -> ServerParamCollectionContract:
        """Get the parameters that the server gives."""

    @abstractmethod
    def with_server_params(self, server: ServerParamCollectionContract) -> Self:
        """Get a copy of the request that carries different server parameters."""

    @abstractmethod
    def get_cookie_params(self) -> CookieParamCollectionContract:
        """Get the cookies that the request carries."""

    @abstractmethod
    def with_cookie_params(self, cookies: CookieParamCollectionContract) -> Self:
        """Get a copy of the request that carries different cookies."""

    @abstractmethod
    def get_query_params(self) -> QueryParamCollectionContract:
        """Get the parameters that the query string carries."""

    @abstractmethod
    def with_query_params(self, query: QueryParamCollectionContract) -> Self:
        """Get a copy of the request that carries a different query string."""

    @abstractmethod
    def get_parsed_body(self) -> ParsedBodyParamCollectionContract:
        """Get the parameters that the body carries."""

    @abstractmethod
    def with_parsed_body(self, params: ParsedBodyParamCollectionContract) -> Self:
        """Get a copy of the request that carries a different body."""

    @abstractmethod
    def get_attributes(self) -> AttributeParamCollectionContract:
        """Get the attributes that the application set on the request."""

    @abstractmethod
    def with_attributes(self, attributes: AttributeParamCollectionContract) -> Self:
        """Get a copy of the request that carries different attributes."""

    @abstractmethod
    def is_xml_http_request(self) -> bool:
        """Get whether a script in the browser made the request."""
