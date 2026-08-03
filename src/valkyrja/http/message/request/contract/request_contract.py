#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self

from valkyrja.http.message.contract.message_contract import MessageContract
from valkyrja.http.message.enum.request_method import RequestMethod
from valkyrja.http.message.uri.contract.uri_contract import UriContract


class RequestContract(MessageContract):
    """The contract for a request that the application answers."""

    @abstractmethod
    def get_request_target(self) -> str:
        """Get the target of the request, as the request line writes it."""

    @abstractmethod
    def with_request_target(self, request_target: str) -> Self:
        """Get a copy of the request that carries a different target."""

    @abstractmethod
    def get_method(self) -> RequestMethod:
        """Get the method of the request."""

    @abstractmethod
    def with_method(self, method: RequestMethod) -> Self:
        """Get a copy of the request that carries a different method."""

    @abstractmethod
    def get_uri(self) -> UriContract:
        """Get the uri of the request."""

    @abstractmethod
    def with_uri(self, uri: UriContract, preserve_host: bool = False) -> Self:
        """Get a copy of the request that asks for a different uri."""
