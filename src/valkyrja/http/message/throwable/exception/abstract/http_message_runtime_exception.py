#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.throwable.contract.http_message_throwable import HttpMessageThrowable
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import (
    ValkyrjaRuntimeException,
)


class HttpMessageRuntimeException(ValkyrjaRuntimeException, HttpMessageThrowable):
    """The base runtime exception of the Http Message subcomponent."""

    _valkyrja_abstract = True
