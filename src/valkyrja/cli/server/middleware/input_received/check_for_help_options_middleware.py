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
from valkyrja.cli.middleware.contract.input_received_middleware_contract import (
    InputReceivedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.input_received_handler_contract import (
    InputReceivedHandlerContract,
)


class CheckForHelpOptionsMiddleware(InputReceivedMiddlewareContract):
    """Sends the input to the help command when the user asks for help."""

    def __init__(self, command_name: str, option_name: str, option_short_name: str) -> None:
        self._command_name = command_name
        self._option_name = option_name
        self._option_short_name = option_short_name

    @override
    def input_received(
        self, input_: InputContract, handler: InputReceivedHandlerContract
    ) -> InputContract | OutputContract:
        if input_.has_option(self._option_short_name) or input_.has_option(self._option_name):
            input_ = input_.with_command_name(self._command_name).with_options()

        return handler.input_received(input_)
