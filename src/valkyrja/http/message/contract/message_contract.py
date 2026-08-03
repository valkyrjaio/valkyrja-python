#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.http.message.enum.protocol_version import ProtocolVersion
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.stream.contract.stream_contract import StreamContract


class MessageContract(ABC):
    """The contract that a request and a response share."""

    @abstractmethod
    def get_protocol_version(self) -> ProtocolVersion:
        """Get the version of HTTP that the message speaks."""

    @abstractmethod
    def with_protocol_version(self, version: ProtocolVersion) -> Self:
        """Get a copy of the message that speaks a different version."""

    @abstractmethod
    def get_headers(self) -> HeaderCollectionContract:
        """Get the headers of the message."""

    @abstractmethod
    def with_headers(self, headers: HeaderCollectionContract) -> Self:
        """Get a copy of the message that carries different headers."""

    @abstractmethod
    def get_body(self) -> StreamContract:
        """Get the body of the message."""

    @abstractmethod
    def with_body(self, body: StreamContract) -> Self:
        """Get a copy of the message that carries a different body."""
