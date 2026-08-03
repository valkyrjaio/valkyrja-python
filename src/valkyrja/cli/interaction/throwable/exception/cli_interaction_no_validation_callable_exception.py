#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.throwable.exception.abstract.cli_interaction_runtime_exception import (
    CliInteractionRuntimeException,
)


class CliInteractionNoValidationCallableException(CliInteractionRuntimeException):
    """An answer has no validator, and a caller asked for one."""
