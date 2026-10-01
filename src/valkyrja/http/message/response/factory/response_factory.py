#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, override

from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.response.contract.json_response_contract import JsonResponseContract
from valkyrja.http.message.response.contract.redirect_response_contract import (
    RedirectResponseContract,
)
from valkyrja.http.message.response.contract.response_contract import ResponseContract
from valkyrja.http.message.response.contract.text_response_contract import TextResponseContract
from valkyrja.http.message.response.factory.contract.response_factory_contract import (
    ResponseFactoryContract,
)
from valkyrja.http.message.response.json_response import JsonResponse
from valkyrja.http.message.response.redirect_response import RedirectResponse
from valkyrja.http.message.response.response import Response
from valkyrja.http.message.response.text_response import TextResponse
from valkyrja.http.message.uri.factory.uri_factory import UriFactory


class ResponseFactory(ResponseFactoryContract):
    @override
    def create_response(
        self,
        content: str = "",
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> ResponseContract:
        return Response.create(content=content, status_code=status_code, headers=headers)

    @override
    def create_text_response(
        self,
        content: str = "",
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> TextResponseContract:
        return TextResponse(text=content, status_code=status_code, headers=headers)

    @override
    def create_json_response(
        self,
        data: dict[str, Any] | None = None,
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> JsonResponseContract:
        return JsonResponse.create_from_data(data=data, status_code=status_code, headers=headers)

    @override
    def create_jsonp_response(
        self,
        callback: str,
        data: dict[str, Any] | None = None,
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> JsonResponseContract:
        return self.create_json_response(data, status_code, headers).with_callback(callback)

    @override
    def create_redirect_response(
        self,
        uri: str = "/",
        status_code: StatusCode = StatusCode.FOUND,
        headers: HeaderCollectionContract | None = None,
    ) -> RedirectResponseContract:
        return RedirectResponse.create_from_uri(
            uri=UriFactory.from_string(uri), status_code=status_code, headers=headers
        )
