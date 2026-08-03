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


class CliInteractionConfig(CliInteractionConfigContract):
    """The default configuration of the Cli Interaction subcomponent."""

    def __init__(self, is_quiet: bool = False, is_interactive: bool = True, is_silent: bool = False) -> None:
        self._is_quiet = is_quiet
        self._is_interactive = is_interactive
        self._is_silent = is_silent

    @property
    @override
    def is_quiet(self) -> bool:
        return self._is_quiet

    @is_quiet.setter
    @override
    def is_quiet(self, is_quiet: bool) -> None:
        self._is_quiet = is_quiet

    @property
    @override
    def is_interactive(self) -> bool:
        return self._is_interactive

    @is_interactive.setter
    @override
    def is_interactive(self, is_interactive: bool) -> None:
        self._is_interactive = is_interactive

    @property
    @override
    def is_silent(self) -> bool:
        return self._is_silent

    @is_silent.setter
    @override
    def is_silent(self, is_silent: bool) -> None:
        self._is_silent = is_silent
