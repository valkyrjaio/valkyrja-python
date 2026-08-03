#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.cli.interaction.data.contract.cli_interaction_config_contract import (
    CliInteractionConfigContract,
)
from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.contract.input_received_middleware_contract import (
    InputReceivedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.input_received_handler_contract import (
    InputReceivedHandlerContract,
)


class CheckGlobalInteractionOptionsMiddleware(InputReceivedMiddlewareContract):
    """Reads the options that change how the output talks to the user."""

    def __init__(
        self,
        config: CliInteractionConfigContract,
        no_interaction_option_name: str,
        no_interaction_option_short_name: str,
        quiet_option_name: str,
        quiet_option_short_name: str,
        silent_option_name: str,
        silent_option_short_name: str,
    ) -> None:
        self._config = config
        self._no_interaction_option_name = no_interaction_option_name
        self._no_interaction_option_short_name = no_interaction_option_short_name
        self._quiet_option_name = quiet_option_name
        self._quiet_option_short_name = quiet_option_short_name
        self._silent_option_name = silent_option_name
        self._silent_option_short_name = silent_option_short_name

    @override
    def input_received(
        self, input_: InputContract, handler: InputReceivedHandlerContract
    ) -> InputContract | OutputContract:
        self._set_is_interactive(input_)
        self._set_is_quiet(input_)
        self._set_is_silent(input_)

        return handler.input_received(input_)

    def _set_is_interactive(self, input_: InputContract) -> None:
        """Stop the output asking a question when the user says so."""
        if self._has_option(input_, self._no_interaction_option_name, self._no_interaction_option_short_name):
            self._config.is_interactive = False

    def _set_is_quiet(self, input_: InputContract) -> None:
        """Drop a message of low importance when the user says so."""
        if self._has_option(input_, self._quiet_option_name, self._quiet_option_short_name):
            self._config.is_quiet = True

    def _set_is_silent(self, input_: InputContract) -> None:
        """Write no message at all when the user says so."""
        if self._has_option(input_, self._silent_option_name, self._silent_option_short_name):
            self._config.is_silent = True

    @staticmethod
    def _has_option(input_: InputContract, name: str, short_name: str) -> bool:
        """Get whether the input carries an option by either of its names."""
        return input_.has_option(short_name) or input_.has_option(name)
