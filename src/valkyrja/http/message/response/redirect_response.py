#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import TYPE_CHECKING, Self, override

from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.response.contract.redirect_response_contract import (
    RedirectResponseContract,
)
from valkyrja.http.message.response.response import Response
from valkyrja.http.message.response.throwable.exception.http_response_invalid_redirect_status_code_exception import (
    HttpResponseInvalidRedirectStatusCodeException,
)
from valkyrja.http.message.uri.contract.uri_contract import UriContract
from valkyrja.http.message.uri.enum.scheme import Scheme
from valkyrja.http.message.uri.factory.uri_factory import UriFactory
from valkyrja.http.message.uri.uri import Uri

if TYPE_CHECKING:
    from valkyrja.http.message.request.contract.server_request_contract import (
        ServerRequestContract,
    )


class RedirectResponse(Response, RedirectResponseContract):
    def __init__(
        self,
        uri: UriContract | None = None,
        status_code: StatusCode = StatusCode.FOUND,
        headers: HeaderCollectionContract | None = None,
    ) -> None:
        if not status_code.is_redirect():
            raise HttpResponseInvalidRedirectStatusCodeException(
                f"Invalid redirect status code {status_code.value} used."
            )

        self._uri: UriContract = uri if uri is not None else Uri(path="/")

        headers = headers if headers is not None else HeaderCollection()

        super().__init__(
            status_code=status_code,
            headers=headers.with_header(Header(HeaderName.LOCATION, str(self._uri))),
        )

    @classmethod
    def create_from_uri(
        cls,
        uri: UriContract | None = None,
        status_code: StatusCode = StatusCode.FOUND,
        headers: HeaderCollectionContract | None = None,
    ) -> RedirectResponse:
        """Build a response that sends the caller to one uri."""
        return cls(uri=uri, status_code=status_code, headers=headers)

    @override
    def get_uri(self) -> UriContract:
        return self._uri

    @override
    def with_uri(self, uri: UriContract) -> Self:
        new = copy(self)
        new._uri = uri
        new._headers = self._headers.with_header(Header(HeaderName.LOCATION, str(uri)))

        return new

    @override
    def secure(self, path: str, request: ServerRequestContract) -> Self:
        # The host and the port go in apart from each other. A combined `host:port`
        # would reach the host filter, which encodes the colon it holds.
        request_uri = request.get_uri()

        return self.with_uri(
            Uri(scheme=Scheme.HTTPS, host=request_uri.get_host(), port=request_uri.get_port(), path=path)
        )

    @override
    def back(self, request: ServerRequestContract) -> Self:
        referer = request.get_headers().get_header_line(HeaderName.REFERER) or "/"
        referer_uri = UriFactory.from_string(referer)

        # A referer that names another host would send the caller off the site, so
        # the response sends it to the root instead.
        return self.with_uri(referer_uri if self._is_internal_uri(request, referer_uri) else Uri(path="/"))

    @staticmethod
    def _is_internal_uri(request: ServerRequestContract, uri: UriContract) -> bool:
        """Get whether a uri names this host, or names no host at all."""
        host = uri.get_host()

        return host == "" or host == request.get_uri().get_host()
