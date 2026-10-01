#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import json
from copy import copy
from typing import Any, Self, override

from valkyrja.http.message.constant.content_type_value import ContentTypeValue
from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.protocol_version import ProtocolVersion
from valkyrja.http.message.enum.request_method import RequestMethod
from valkyrja.http.message.file.collection.contract.uploaded_file_collection_contract import (
    UploadedFileCollectionContract,
)
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.param.contract.attribute_param_collection_contract import (
    AttributeParamCollectionContract,
)
from valkyrja.http.message.param.contract.cookie_param_collection_contract import (
    CookieParamCollectionContract,
)
from valkyrja.http.message.param.contract.parsed_body_param_collection_contract import (
    ParsedBodyParamCollectionContract,
)
from valkyrja.http.message.param.contract.parsed_json_param_collection_contract import (
    ParsedJsonParamCollectionContract,
)
from valkyrja.http.message.param.contract.query_param_collection_contract import (
    QueryParamCollectionContract,
)
from valkyrja.http.message.param.contract.server_param_collection_contract import (
    ServerParamCollectionContract,
)
from valkyrja.http.message.param.parsed_json_param_collection import ParsedJsonParamCollection
from valkyrja.http.message.request.contract.json_server_request_contract import (
    JsonServerRequestContract,
)
from valkyrja.http.message.request.server_request import ServerRequest
from valkyrja.http.message.request.throwable.exception.http_request_invalid_json_exception import (
    HttpRequestInvalidJsonException,
)
from valkyrja.http.message.stream.contract.stream_contract import StreamContract
from valkyrja.http.message.uri.contract.uri_contract import UriContract


class JsonServerRequest(ServerRequest, JsonServerRequestContract):
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
        uploaded_files: UploadedFileCollectionContract | None = None,
        parsed_json: ParsedJsonParamCollectionContract | None = None,
    ) -> None:
        super().__init__(
            uri,
            method,
            body,
            headers,
            protocol_version,
            server,
            cookies,
            query,
            parsed_body,
            attributes,
            uploaded_files,
        )

        self._parsed_json: ParsedJsonParamCollectionContract = (
            parsed_json if parsed_json is not None else ParsedJsonParamCollection()
        )

        if self._carries_json():
            self._parsed_json = self._get_parsed_json_from_body()

    @override
    def get_parsed_json(self) -> ParsedJsonParamCollectionContract:
        return self._parsed_json

    @override
    def with_parsed_json(self, params: ParsedJsonParamCollectionContract) -> Self:
        new = copy(self)
        new._parsed_json = params

        return new

    def _carries_json(self) -> bool:
        """Get whether the content type of the request names json."""
        return ContentTypeValue.APPLICATION_JSON in self._headers.get_header_line(HeaderName.CONTENT_TYPE)

    def _get_parsed_json_from_body(self) -> ParsedJsonParamCollectionContract:
        """Read the body as json.

        An empty body carries no json, and it leaves the collection as it is.
        """
        contents = str(self.get_body())

        if contents == "":
            return self._parsed_json

        try:
            decoded: Any = json.loads(contents)
        except ValueError as exception:
            raise HttpRequestInvalidJsonException("The body of the request holds no json") from exception

        if not isinstance(decoded, dict):
            raise HttpRequestInvalidJsonException("The json of the request names no object")

        return ParsedJsonParamCollection(decoded)
