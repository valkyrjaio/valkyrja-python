#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.throwable.exception.abstract.http_message_invalid_argument_exception import (
    HttpMessageInvalidArgumentException,
)
from valkyrja.http.message.uri.throwable.contract.http_uri_throwable import (
    HttpUriThrowable,
)


class HttpUriInvalidArgumentException(HttpMessageInvalidArgumentException, HttpUriThrowable):
    _valkyrja_abstract = True
