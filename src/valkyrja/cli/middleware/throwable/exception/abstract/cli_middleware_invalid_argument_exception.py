#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.middleware.throwable.contract.cli_middleware_throwable import (
    CliMiddlewareThrowable,
)
from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)


class CliMiddlewareInvalidArgumentException(ValkyrjaInvalidArgumentException, CliMiddlewareThrowable):
    _valkyrja_abstract = True
