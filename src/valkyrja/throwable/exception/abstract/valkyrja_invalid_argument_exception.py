#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable


class ValkyrjaInvalidArgumentException(ValkyrjaThrowable, ValueError):
    """The base invalid argument exception for every component.

    The name keeps parity with the other ports. Python spells the language root
    `ValueError`, so the class extends `ValueError` and a caller catches an
    invalid argument the way the language does.
    """

    # `ValkyrjaThrowable` comes first, because the method resolution order
    # decides which `__new__` runs. `ValueError` inherits a `__new__` that
    # constructs any class, so a base list that puts `ValueError` first defeats
    # the abstract guard on `ValkyrjaThrowable`.
    _valkyrja_abstract = True
