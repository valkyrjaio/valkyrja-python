#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.throwable.contract.http_message_throwable import HttpMessageThrowable
from valkyrja.http.throwable.exception.abstract.http_invalid_argument_exception import (
    HttpInvalidArgumentException,
)


class HttpMessageInvalidArgumentException(HttpInvalidArgumentException, HttpMessageThrowable):
    """The base invalid argument exception of the Http Message subcomponent."""

    _valkyrja_abstract = True
