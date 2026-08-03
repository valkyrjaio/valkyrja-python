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
from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.value.contract.cookie_contract import CookieContract


class ResponseContract(MessageContract):
    """The contract for the response that the application answers with."""

    @abstractmethod
    def get_status_code(self) -> StatusCode:
        """Get the status code of the response."""

    @abstractmethod
    def with_status_code(self, code: StatusCode) -> Self:
        """Get a copy of the response that carries a different status code."""

    @abstractmethod
    def get_reason_phrase(self) -> str:
        """Get the text that goes with the status code."""

    @abstractmethod
    def with_reason_phrase(self, reason_phrase: str) -> Self:
        """Get a copy of the response that carries a different reason phrase."""

    @abstractmethod
    def with_cookie(self, cookie: CookieContract) -> Self:
        """Get a copy of the response that sets one more cookie."""

    @abstractmethod
    def without_cookie(self, cookie: CookieContract) -> Self:
        """Get a copy of the response that tells the browser to drop a cookie."""

    @abstractmethod
    def send_http_line(self) -> Self:
        """Write the status line of the response."""

    @abstractmethod
    def send_headers(self) -> Self:
        """Write each header of the response."""

    @abstractmethod
    def send_body(self) -> Self:
        """Write the body of the response."""

    @abstractmethod
    def send(self) -> Self:
        """Write the whole response."""
