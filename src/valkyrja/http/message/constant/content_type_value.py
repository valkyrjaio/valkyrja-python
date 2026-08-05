#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class ContentTypeValue:
    """The value that a `Content-Type` header carries."""

    TEXT_HTML: Final[str] = "text/html"
    TEXT_PLAIN: Final[str] = "text/plain"
    APPLICATION_JSON: Final[str] = "application/json"
    TEXT_HTML_UTF8: Final[str] = "text/html; charset=utf-8"
    TEXT_PLAIN_UTF8: Final[str] = "text/plain; charset=utf-8"
