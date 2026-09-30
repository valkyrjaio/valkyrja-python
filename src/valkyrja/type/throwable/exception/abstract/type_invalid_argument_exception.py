#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)
from valkyrja.type.throwable.contract.type_throwable import TypeThrowable


class TypeInvalidArgumentException(ValkyrjaInvalidArgumentException, TypeThrowable):
    _valkyrja_abstract = True
