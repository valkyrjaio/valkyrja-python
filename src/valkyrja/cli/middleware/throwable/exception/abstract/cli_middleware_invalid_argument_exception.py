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
from valkyrja.cli.throwable.exception.abstract.cli_invalid_argument_exception import (
    CliInvalidArgumentException,
)


class CliMiddlewareInvalidArgumentException(CliInvalidArgumentException, CliMiddlewareThrowable):
    _valkyrja_abstract = True
