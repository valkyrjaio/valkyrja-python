#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import TYPE_CHECKING, Self

from valkyrja.http.message.response.contract.response_contract import ResponseContract
from valkyrja.http.message.uri.contract.uri_contract import UriContract

if TYPE_CHECKING:
    from valkyrja.http.message.request.contract.server_request_contract import (
        ServerRequestContract,
    )


class RedirectResponseContract(ResponseContract):
    @abstractmethod
    def get_uri(self) -> UriContract:
        """Get the uri that the response sends the caller to."""

    @abstractmethod
    def with_uri(self, uri: UriContract) -> Self:
        """Get a copy of the response that sends the caller somewhere else."""

    @abstractmethod
    def secure(self, path: str, request: ServerRequestContract) -> Self:
        """Get a copy that sends the caller to one path of the secure host."""

    @abstractmethod
    def back(self, request: ServerRequestContract) -> Self:
        """Get a copy that sends the caller to the page it came from."""
