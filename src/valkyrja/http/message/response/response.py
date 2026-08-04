#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import sys
from copy import copy
from typing import Self, override

from valkyrja.http.message.abstract.message import Message
from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.enum.protocol_version import ProtocolVersion
from valkyrja.http.message.enum.status_code import StatusCode
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.header.value.contract.cookie_contract import CookieContract
from valkyrja.http.message.response.contract.response_contract import ResponseContract
from valkyrja.http.message.stream.contract.stream_contract import StreamContract


class Response(Message, ResponseContract):
    """The response that the application answers with."""

    def __init__(
        self,
        body: StreamContract | None = None,
        status_code: StatusCode = StatusCode.OK,
        headers: HeaderCollectionContract | None = None,
        protocol_version: ProtocolVersion = ProtocolVersion.V1_1,
    ) -> None:
        super().__init__(body, headers, protocol_version)

        self._status_code = status_code
        self._reason_phrase = status_code.as_phrase()

    @override
    def get_status_code(self) -> StatusCode:
        return self._status_code

    @override
    def with_status_code(self, code: StatusCode) -> Self:
        new = copy(self)
        new._status_code = code
        new._reason_phrase = code.as_phrase()

        return new

    @override
    def get_reason_phrase(self) -> str:
        return self._reason_phrase

    @override
    def with_reason_phrase(self, reason_phrase: str) -> Self:
        new = copy(self)
        new._reason_phrase = reason_phrase

        return new

    @override
    def with_cookie(self, cookie: CookieContract) -> Self:
        return self._with_set_cookie(cookie)

    @override
    def without_cookie(self, cookie: CookieContract) -> Self:
        return self._with_set_cookie(cookie.delete())

    @override
    def send_http_line(self) -> Self:
        self._write(f"HTTP/{self._protocol_version.value} {self._status_code.value} {self._reason_phrase}\n")

        return self

    @override
    def send_headers(self) -> Self:
        for header in self._headers.get_all():
            if header.get_normalized_name() == HeaderName.SET_COOKIE.lower():
                # RFC 7230 forbids joining a `Set-Cookie` field with a comma,
                # because the `Expires` attribute of a cookie holds a comma. Each
                # cookie therefore takes a line of its own.
                for value in header.get_values():
                    self._write(f"{header.get_name()}: {value}\n")

                continue

            self._write(f"{header}\n")

        return self

    @override
    def send_body(self) -> Self:
        self._write(str(self._body))

        return self

    @override
    def send(self) -> Self:
        return self.send_http_line().send_headers().send_body()

    def _with_set_cookie(self, cookie: CookieContract) -> Self:
        """Get a copy that carries one more `Set-Cookie` header.

        A response sets several cookies, so the header takes each cookie as one
        more value rather than replacing the header.
        """
        headers = self._headers
        existing = headers.get(HeaderName.SET_COOKIE).get_values() if headers.has(HeaderName.SET_COOKIE) else []

        return self.with_headers(headers.with_header(Header(HeaderName.SET_COOKIE, *existing, cookie)))

    def _write(self, text: str) -> None:
        """Put the text where a reader sees it.

        The method is a seam. A test overrides it, because a test cannot read
        the headers that a real server writes.
        """
        sys.stdout.write(text)
