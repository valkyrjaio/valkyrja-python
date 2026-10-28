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
    APPLICATION_JSON: Final[str] = "application/json"
    APPLICATION_JAVASCRIPT: Final[str] = "application/javascript"
    APPLICATION_XML: Final[str] = "application/xml"
    APPLICATION_XML_UTF8: Final[str] = "application/xml; charset=utf-8"
    APPLICATION_X_WWW_FORM: Final[str] = "application/x-www-form-urlencoded"
    MULTIPART_FORM_DATA: Final[str] = "multipart/form-data"
    TEXT_HTML: Final[str] = "text/html"
    TEXT_HTML_UTF8: Final[str] = "text/html; charset=utf-8"
    TEXT_JAVASCRIPT: Final[str] = "text/javascript"
    TEXT_PLAIN: Final[str] = "text/plain"
    TEXT_PLAIN_UTF8: Final[str] = "text/plain; charset=utf-8"
