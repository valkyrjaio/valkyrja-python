#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import re

from valkyrja.http.message.header.throwable.exception.http_header_invalid_name_exception import (
    HttpHeaderInvalidNameException,
)
from valkyrja.http.message.header.throwable.exception.http_header_invalid_value_exception import (
    HttpHeaderInvalidValueException,
)

NAME_PATTERN = re.compile(r"[a-zA-Z0-9'`#$%&*+.^_|~!-]+")
"""RFC 7230 section 3.2 names each character that a header name holds."""

INJECTION_PATTERN = re.compile(r"(?:(?<!\r)\n)|(?:\r(?!\n))|(?:\r\n(?![ \t]))")
"""A lone line feed, a lone carriage return, and a fold with no space after it.

Each one splits a response, so a value that holds one is refused.
"""

NON_VISIBLE_PATTERN = re.compile(r"[^\x09\x0a\x0d\x20-\x7e\x80-\xfe]")
"""A character outside the tab, the fold, and the visible ranges."""

FOLD_FOLLOWERS = (" ", "\t")
"""A fold continues a value only when one of these follows it."""


class HeaderFactory:
    @staticmethod
    def is_valid_name(name: str) -> bool:
        """Get whether a header name holds only the characters RFC 7230 allows."""
        return name != "" and NAME_PATTERN.fullmatch(name) is not None

    @staticmethod
    def assert_valid_name(name: str) -> None:
        """Refuse a header name that RFC 7230 does not allow."""
        if not HeaderFactory.is_valid_name(name):
            raise HttpHeaderInvalidNameException(f'"{name}" is not valid header name')

    @staticmethod
    def is_valid_value(value: str) -> bool:
        """Get whether a header value holds only what RFC 7230 allows.

        RFC 7230 allows a visible character, a space, and a horizontal tab. A fold
        is one carriage return and one line feed, and a space or a tab follows it.
        """
        if INJECTION_PATTERN.search(value) is not None:
            return False

        return NON_VISIBLE_PATTERN.search(value) is None

    @staticmethod
    def assert_valid_value(value: str) -> None:
        """Refuse a header value that would split the response."""
        if not HeaderFactory.is_valid_value(value):
            raise HttpHeaderInvalidValueException(f'"{value}" is not valid header value')

    @staticmethod
    def get_filtered_value(value: str) -> str:
        """Get the value with each character that RFC 7230 forbids removed.

        A fold survives, because a fold continues one value. Every other control
        character goes, so no value splits the response.
        """
        filtered: list[str] = []
        index = 0
        length = len(value)

        while index < length:
            character = value[index]

            if character == "\r":
                follows = value[index + 1 : index + 3]

                if len(follows) == 2 and follows[0] == "\n" and follows[1] in FOLD_FOLLOWERS:
                    filtered.append("\r\n")
                    index += 2

                    continue

                index += 1

                continue

            if not HeaderFactory._is_invalid_character(character):
                filtered.append(character)

            index += 1

        return "".join(filtered)

    @staticmethod
    def _is_invalid_character(character: str) -> bool:
        """Get whether one character is one that a header value cannot hold."""
        code = ord(character)

        return (code < 32 and code != 9) or code == 127 or code > 254
