#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import json
from copy import deepcopy
from typing import Any

from valkyrja.http.message.constant.content_type_value import ContentTypeValue
from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.response.contract.json_response_contract import JsonResponseContract
from valkyrja.http.message.response.response import Response
from valkyrja.http.message.stream.stream import Stream


class JsonResponse(Response, JsonResponseContract):
    """A response that carries json."""

    def __init__(
        self,
        data: dict[str, Any] | None = None,
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> None:
        self._data: dict[str, Any] = data if data is not None else {}

        body = Stream()
        body.write(json.dumps(self._data))
        body.rewind()

        headers = headers if headers is not None else HeaderCollection()

        super().__init__(
            body=body,
            status_code=status_code,
            headers=headers.with_header(Header(HeaderName.CONTENT_TYPE, ContentTypeValue.APPLICATION_JSON)),
        )

    def get_data(self) -> dict[str, Any]:
        """Get the data that the response carries.

        The copy is deep. A shallow copy shares a nested list, so a caller that
        appends to it changes the body of the response.
        """
        return deepcopy(self._data)
