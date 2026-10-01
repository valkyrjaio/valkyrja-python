#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Any, Self

from valkyrja.http.message.response.contract.response_contract import ResponseContract


class JsonResponseContract(ResponseContract):
    @abstractmethod
    def get_data(self) -> dict[str, Any]:
        """Get the data that the response carries."""

    @abstractmethod
    def get_body_as_json(self) -> dict[str, Any]:
        """Get the data that the body of the response holds."""

    @abstractmethod
    def with_json_as_body(self, data: dict[str, Any]) -> Self:
        """Get a copy of the response that carries different data."""

    @abstractmethod
    def with_callback(self, callback: str) -> Self:
        """Get a copy of the response that wraps the data in a callback."""

    @abstractmethod
    def without_callback(self) -> Self:
        """Get a copy of the response that carries the data alone."""
