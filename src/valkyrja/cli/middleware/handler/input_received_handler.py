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
from valkyrja.cli.middleware.contract.input_received_middleware_contract import (
    InputReceivedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.abstract.handler import Handler
from valkyrja.cli.middleware.handler.contract.input_received_handler_contract import (
    InputReceivedHandlerContract,
)


class InputReceivedHandler(Handler, InputReceivedHandlerContract):
    """Runs each middleware for a received input."""

    @override
    def input_received(self, input_: InputContract) -> InputContract | OutputContract:
        next_middleware = self._next

        if next_middleware is None:
            return input_

        return cast("InputReceivedMiddlewareContract", self._get_middleware(next_middleware)).input_received(
            input_, self
        )
