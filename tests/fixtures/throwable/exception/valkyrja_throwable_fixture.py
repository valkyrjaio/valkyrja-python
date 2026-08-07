#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable


@final
class ValkyrjaThrowableFixture(ValkyrjaThrowable):
    """A concrete throwable that implements the contract directly.

    The fixture extends neither abstract exception, so a test reaches the
    contract without a categorical base between them.
    """
