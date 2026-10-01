#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.header.throwable.contract.http_header_throwable import (
    HttpHeaderThrowable,
)
from valkyrja.http.message.throwable.exception.abstract.http_message_invalid_argument_exception import (
    HttpMessageInvalidArgumentException,
)


class HttpHeaderInvalidHeaderNameException(HttpMessageInvalidArgumentException, HttpHeaderThrowable):
    pass
