#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self

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
from valkyrja.http.message.response.throwable.exception.http_invalid_redirect_status_code_exception import (
    HttpInvalidRedirectStatusCodeException,
)
from valkyrja.http.message.uri.contract.uri_contract import UriContract
from valkyrja.http.message.uri.uri import Uri


class RedirectResponse(Response, RedirectResponseContract):
    """A response that sends the caller somewhere else."""

    def __init__(
        self,
        uri: UriContract | None = None,
        status_code: StatusCode = StatusCode.FOUND,
        headers: HeaderCollectionContract | None = None,
    ) -> None:
        if not status_code.is_redirect():
            raise HttpInvalidRedirectStatusCodeException(f"Invalid redirect status code {status_code.value} used.")

        self._uri: UriContract = uri if uri is not None else Uri(path="/")

        headers = headers if headers is not None else HeaderCollection()

        super().__init__(
            status_code=status_code,
            headers=headers.with_header(Header(HeaderName.LOCATION, str(self._uri))),
        )

    def get_uri(self) -> UriContract:
        """Get the uri that the response sends the caller to."""
        return self._uri

    def with_uri(self, uri: UriContract) -> Self:
        """Get a copy of the response that sends the caller somewhere else."""
        new = copy(self)
        new._uri = uri
        new._headers = self._headers.with_header(Header(HeaderName.LOCATION, str(uri)))

        return new
