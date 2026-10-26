#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.response.throwable.contract.http_response_throwable import (
    HttpResponseThrowable,
)
from valkyrja.http.message.throwable.exception.abstract.http_message_invalid_argument_exception import (
    HttpMessageInvalidArgumentException,
)


class HttpResponseInvalidArgumentException(HttpMessageInvalidArgumentException, HttpResponseThrowable):
    _valkyrja_abstract = True
