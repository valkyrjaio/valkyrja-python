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


class CliInteractionExpectedQuestionOutputException(CliInteractionRuntimeException):
    """A question writer got an output that holds no question."""
