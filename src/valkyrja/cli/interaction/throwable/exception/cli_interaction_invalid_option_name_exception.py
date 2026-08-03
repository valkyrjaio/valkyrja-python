#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.throwable.exception.abstract.cli_interaction_invalid_argument_exception import (
    CliInteractionInvalidArgumentException,
)


class CliInteractionInvalidOptionNameException(CliInteractionInvalidArgumentException):
    """An option name is not valid."""
