#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.response.contract.empty_response_contract import EmptyResponseContract
from valkyrja.http.message.response.response import Response
from valkyrja.http.message.stream.enum.mode import Mode
from valkyrja.http.message.stream.stream import Stream


class EmptyResponse(Response, EmptyResponseContract):
    """A response that carries no body."""

    def __init__(self, headers: HeaderCollectionContract | None = None) -> None:
        super().__init__(body=Stream(mode=Mode.READ), status_code=StatusCode.NO_CONTENT, headers=headers)
