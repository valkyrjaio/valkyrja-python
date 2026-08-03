#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class HeaderName:
    """The name of each header that the framework reads or writes."""

    ACCEPT: Final[str] = "Accept"
    ACCEPT_CHARSET: Final[str] = "Accept-Charset"
    ACCEPT_ENCODING: Final[str] = "Accept-Encoding"
    ACCEPT_LANGUAGE: Final[str] = "Accept-Language"
    ACCEPT_RANGES: Final[str] = "Accept-Ranges"
    AGE: Final[str] = "Age"
    ALLOW: Final[str] = "Allow"
    AUTHORIZATION: Final[str] = "Authorization"
    CACHE_CONTROL: Final[str] = "Cache-Control"
    CONNECTION: Final[str] = "Connection"
    CONTENT_ENCODING: Final[str] = "Content-Encoding"
    CONTENT_LANGUAGE: Final[str] = "Content-Language"
    CONTENT_LENGTH: Final[str] = "Content-Length"
    CONTENT_LOCATION: Final[str] = "Content-Location"
    CONTENT_MD5: Final[str] = "Content-MD5"
    CONTENT_RANGE: Final[str] = "Content-Range"
    CONTENT_TYPE: Final[str] = "Content-Type"
    DATE: Final[str] = "Date"
    E_TAG: Final[str] = "ETag"
    EXPECT: Final[str] = "Expect"
    EXPIRES: Final[str] = "Expires"
    FROM: Final[str] = "From"
    HOST: Final[str] = "Host"
    IF_MATCH: Final[str] = "If-Match"
    IF_MODIFIED_SINCE: Final[str] = "If-Modified-Since"
    IF_NONE_MATCH: Final[str] = "If-None-Match"
    IF_RANGE: Final[str] = "If-Range"
    IF_UNMODIFIED_SINCE: Final[str] = "If-Unmodified-Since"
    LAST_MODIFIED: Final[str] = "Last-Modified"
    LOCATION: Final[str] = "Location"
    MAX_FORWARDS: Final[str] = "Max-Forwards"
    PRAGMA: Final[str] = "Pragma"
    PROXY_AUTHENTICATE: Final[str] = "Proxy-Authenticate"
    PROXY_AUTHORIZATION: Final[str] = "Proxy-Authorization"
    RANGE: Final[str] = "Range"
    REFERER: Final[str] = "Referer"
    RETRY_AFTER: Final[str] = "Retry-After"
    SERVER: Final[str] = "Server"
    SET_COOKIE: Final[str] = "Set-Cookie"
    TE: Final[str] = "TE"
    TRAILER: Final[str] = "Trailer"
    TRANSFER_ENCODING: Final[str] = "Transfer-Encoding"
    UPGRADE: Final[str] = "Upgrade"
    USER_AGENT: Final[str] = "User-Agent"
    VARY: Final[str] = "Vary"
    VIA: Final[str] = "Via"
    WARNING: Final[str] = "Warning"
    WWW_AUTHENTICATE: Final[str] = "WWW-Authenticate"
    X_REQUESTED_WITH: Final[str] = "X-Requested-With"
