#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.throwable.handler.contract.throwable_handler_contract import ThrowableHandlerContract


@final
class ThrowableHandlerFixture(ThrowableHandlerContract):
    """A handler that records the call instead of changing the interpreter."""

    def __init__(self) -> None:
        self.enabled = False
        self.display_errors = False

    @override
    def enable(self, display_errors: bool = False) -> None:
        self.enabled = True
        self.display_errors = display_errors
