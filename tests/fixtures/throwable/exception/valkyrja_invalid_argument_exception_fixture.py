#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)


@final
class ValkyrjaInvalidArgumentExceptionFixture(ValkyrjaInvalidArgumentException):
    """A concrete invalid argument exception, because the base class is abstract."""
