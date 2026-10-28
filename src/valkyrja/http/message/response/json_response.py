#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy, deepcopy
from typing import Any, Self, override

from valkyrja.http.message.constant.content_type_value import ContentTypeValue
from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.response.contract.json_response_contract import JsonResponseContract
from valkyrja.http.message.response.factory.json_encoder import JsonEncoder
from valkyrja.http.message.response.response import Response
from valkyrja.http.message.response.throwable.exception.http_response_invalid_callback_exception import (
    HttpResponseInvalidCallbackException,
)
from valkyrja.http.message.stream.stream import Stream


class JsonResponse(Response, JsonResponseContract):
    def __init__(
        self,
        data: dict[str, Any] | None = None,
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> None:
        self._data: dict[str, Any] = deepcopy(data) if data is not None else {}

        headers = headers if headers is not None else HeaderCollection()

        super().__init__(
            body=self._get_body_for(self._data),
            status_code=status_code,
            headers=headers.with_header(Header(HeaderName.CONTENT_TYPE, ContentTypeValue.APPLICATION_JSON)),
        )

    @classmethod
    def create_from_data(
        cls,
        data: dict[str, Any] | None = None,
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> JsonResponse:
        """Build a response whose body carries the data as json."""
        return cls(data=data, status_code=status_code, headers=headers)

    @override
    def get_data(self) -> dict[str, Any]:
        """Get the data that the response carries.

        The copy is deep. A shallow copy shares a nested list, so a caller that
        appends to it changes the body of the response.
        """
        return deepcopy(self._data)

    @override
    def get_body_as_json(self) -> dict[str, Any]:
        body = self.get_body()
        body.rewind()
        decoded: dict[str, Any] = JsonEncoder.get_decoded(body.get_contents().decode("utf-8"))
        body.rewind()

        return decoded

    @override
    def with_json_as_body(self, data: dict[str, Any]) -> Self:
        new = copy(self)
        new._data = deepcopy(data)

        return new.with_body(self._get_body_for(new._data))

    @override
    def with_callback(self, callback: str) -> Self:
        self._verify_callback(callback)

        body = Stream()
        body.write(f"/**/{callback}({JsonEncoder.get_encoded(self._data)});")
        body.rewind()

        # The content type is `text/javascript`, which an older browser also reads.
        new = self.with_headers(
            self._headers.with_header(Header(HeaderName.CONTENT_TYPE, ContentTypeValue.TEXT_JAVASCRIPT))
        )

        return new.with_body(body)

    @override
    def without_callback(self) -> Self:
        new = self.with_headers(
            self._headers.with_header(Header(HeaderName.CONTENT_TYPE, ContentTypeValue.APPLICATION_JSON))
        )

        return new.with_body(self._get_body_for(self._data))

    @staticmethod
    def _get_body_for(data: dict[str, Any]) -> Stream:
        """Build the body that carries the data as json."""
        body = Stream()
        body.write(JsonEncoder.get_encoded(data))
        body.rewind()

        return body

    @staticmethod
    def _verify_callback(callback: str) -> None:
        """Refuse a callback name that javascript cannot call.

        A name holds several parts, and a dot separates one part from the next, so
        each part passes the test on its own.
        """
        for part in callback.split("."):
            if part == "" or not part[0].isidentifier() or not part.isidentifier():
                raise HttpResponseInvalidCallbackException("The callback name is not valid.")
