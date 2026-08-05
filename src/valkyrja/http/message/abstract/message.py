#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.contract.message_contract import MessageContract
from valkyrja.http.message.enum.protocol_version import ProtocolVersion
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.stream.contract.stream_contract import StreamContract
from valkyrja.http.message.stream.stream import Stream


class Message(MessageContract):
    """The state that a request and a response share."""

    def __init__(
        self,
        body: StreamContract | None = None,
        headers: HeaderCollectionContract | None = None,
        protocol_version: ProtocolVersion = ProtocolVersion.V1_1,
    ) -> None:
        self._body: StreamContract = body if body is not None else Stream()
        self._headers: HeaderCollectionContract = headers if headers is not None else HeaderCollection()
        self._protocol_version = protocol_version

    @override
    def get_protocol_version(self) -> ProtocolVersion:
        return self._protocol_version

    @override
    def with_protocol_version(self, version: ProtocolVersion) -> Self:
        new = copy(self)
        new._protocol_version = version

        return new

    @override
    def get_headers(self) -> HeaderCollectionContract:
        return self._headers

    @override
    def with_headers(self, headers: HeaderCollectionContract) -> Self:
        new = copy(self)
        new._headers = headers

        return new

    @override
    def get_body(self) -> StreamContract:
        return self._body

    @override
    def with_body(self, body: StreamContract) -> Self:
        new = copy(self)
        new._body = body

        return new
