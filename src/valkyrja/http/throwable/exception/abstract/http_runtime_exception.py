#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.throwable.contract.http_throwable import HttpThrowable
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import (
    ValkyrjaRuntimeException,
)


class HttpRuntimeException(ValkyrjaRuntimeException, HttpThrowable):
    """The base runtime exception of the Http component."""

    _valkyrja_abstract = True
