#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable


class ValkyrjaInvalidArgumentException(ValkyrjaThrowable, ValueError):
    # `ValkyrjaThrowable` comes first, because `ValueError` inherits a `__new__`
    # that constructs any class and defeats the abstract guard.
    _valkyrja_abstract = True
