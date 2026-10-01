#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.stream.throwable.exception.abstract.http_stream_runtime_exception import (
    HttpStreamRuntimeException,
)


class HttpStreamUnreadableStreamException(HttpStreamRuntimeException):
    pass
