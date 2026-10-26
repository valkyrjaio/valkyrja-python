#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.request.throwable.exception.abstract.http_request_invalid_argument_exception import (
    HttpRequestInvalidArgumentException,
)


class HttpRequestInvalidRequestTargetException(HttpRequestInvalidArgumentException):
    pass
