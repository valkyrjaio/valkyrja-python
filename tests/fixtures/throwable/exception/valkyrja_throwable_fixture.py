#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable
from valkyrja.throwable.factory.throwable_factory import ThrowableFactory


@final
class ValkyrjaThrowableFixture(ValkyrjaThrowable):
    """A concrete throwable that implements the contract directly.

    The fixture extends neither abstract exception, so a test reaches the
    contract without a categorical base between them.
    """

    @override
    def get_trace_code(self) -> str:
        return ThrowableFactory.get_trace_code(self)
