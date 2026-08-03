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


class CliInteractionInvalidEmptyValueException(CliInteractionInvalidArgumentException):
    """A value is empty, and the caller needs a value."""
