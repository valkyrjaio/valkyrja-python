#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.contract.header_contract import HeaderContract


class HeaderCollection(HeaderCollectionContract):
    """The headers that a message carries, keyed by the name in lower case.

    A header name is case insensitive, so the collection keys each one by its
    normalized name. A caller reads `Content-Type` and `content-type` alike.
    """

    def __init__(self, *headers: HeaderContract) -> None:
        self._headers: dict[str, HeaderContract] = {header.get_normalized_name(): header for header in headers}

    @override
    def has(self, name: str) -> bool:
        return name.lower() in self._headers

    @override
    def get(self, name: str) -> HeaderContract:
        return self._headers[name.lower()]

    @override
    def get_header_line(self, name: str) -> str:
        if not self.has(name):
            return ""

        return self.get(name).get_header_line()

    @override
    def get_all(self) -> list[HeaderContract]:
        return list(self._headers.values())

    @override
    def get_only(self, *names: str) -> list[HeaderContract]:
        wanted = {name.lower() for name in names}

        return [header for key, header in self._headers.items() if key in wanted]

    @override
    def get_all_except(self, *names: str) -> list[HeaderContract]:
        unwanted = {name.lower() for name in names}

        return [header for key, header in self._headers.items() if key not in unwanted]

    @override
    def with_header(self, header: HeaderContract) -> Self:
        new = self._copy()
        new._headers[header.get_normalized_name()] = header

        return new

    @override
    def without_header(self, name: str) -> Self:
        new = self._copy()
        new._headers.pop(name.lower(), None)

        return new

    def _copy(self) -> Self:
        """Get a copy that holds its own map of headers."""
        new = copy(self)
        new._headers = dict(self._headers)

        return new
