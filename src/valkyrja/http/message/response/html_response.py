#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.constant.content_type_value import ContentTypeValue
from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.response.contract.html_response_contract import HtmlResponseContract
from valkyrja.http.message.response.response import Response
from valkyrja.http.message.stream.stream import Stream


class HtmlResponse(Response, HtmlResponseContract):
    """A response that carries html."""

    def __init__(
        self,
        html: str = "",
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> None:
        body = Stream()
        body.write(html)
        body.rewind()

        headers = headers if headers is not None else HeaderCollection()

        super().__init__(
            body=body,
            status_code=status_code,
            headers=headers.with_header(Header(HeaderName.CONTENT_TYPE, ContentTypeValue.TEXT_HTML_UTF8)),
        )
