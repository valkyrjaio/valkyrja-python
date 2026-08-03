#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.contract.throwable_caught_middleware_contract import (
    ThrowableCaughtMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)


class OutputThrowableCaughtMiddleware(ThrowableCaughtMiddlewareContract):
    """Writes the output that reports a throwable, then stops the chain."""

    @override
    def throwable_caught(
        self,
        input_: InputContract,
        output: OutputContract,
        throwable: BaseException,
        handler: ThrowableCaughtHandlerContract,
    ) -> OutputContract:
        return output.write_messages()
