#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Any

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


class ResponseFactoryContract(ABC):
    @abstractmethod
    def create_response(
        self,
        content: str = "",
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> ResponseContract:
        """Build a response whose body carries the content."""

    @abstractmethod
    def create_text_response(
        self,
        content: str = "",
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> TextResponseContract:
        """Build a response that carries plain text."""

    @abstractmethod
    def create_json_response(
        self,
        data: dict[str, Any] | None = None,
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> JsonResponseContract:
        """Build a response that carries json."""

    @abstractmethod
    def create_jsonp_response(
        self,
        callback: str,
        data: dict[str, Any] | None = None,
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
    ) -> JsonResponseContract:
        """Build a response that carries json inside a callback."""

    @abstractmethod
    def create_redirect_response(
        self,
        uri: str = "/",
        status_code: StatusCode = StatusCode.FOUND,
        headers: HeaderCollectionContract | None = None,
    ) -> RedirectResponseContract:
        """Build a response that sends the caller to one uri."""
