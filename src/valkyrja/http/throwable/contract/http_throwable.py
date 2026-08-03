#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC

from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable


class HttpThrowable(ValkyrjaThrowable, ABC):
    """The contract that every throwable the Http component raises implements."""

    _valkyrja_abstract = True
