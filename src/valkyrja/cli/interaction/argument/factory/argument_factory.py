#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.cli.interaction.argument.argument import Argument
from valkyrja.cli.interaction.argument.contract.argument_contract import ArgumentContract


@final
class ArgumentFactory:
    """Builds an argument from what the user typed."""

    @staticmethod
    def from_arg(arg: str) -> ArgumentContract:
        """Build an argument from one item of the command line."""
        return Argument(arg)
