#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import cast, override

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.contract.throwable_caught_middleware_contract import (
    ThrowableCaughtMiddlewareContract,
)
from valkyrja.cli.middleware.handler.abstract.handler import Handler
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)


class ThrowableCaughtHandler(Handler, ThrowableCaughtHandlerContract):
    """Runs each middleware for a throwable that the application caught."""

    @override
    def throwable_caught(
        self, input_: InputContract, output: OutputContract, throwable: BaseException
    ) -> OutputContract:
        next_middleware = self._next

        if next_middleware is None:
            return output

        return cast("ThrowableCaughtMiddlewareContract", self._get_middleware(next_middleware)).throwable_caught(
            input_, output, throwable, self
        )
