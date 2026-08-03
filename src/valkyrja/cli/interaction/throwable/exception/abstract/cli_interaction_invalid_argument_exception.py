#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.throwable.contract.cli_interaction_throwable import (
    CliInteractionThrowable,
)
from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)


class CliInteractionInvalidArgumentException(ValkyrjaInvalidArgumentException, CliInteractionThrowable):
    """The base invalid argument exception of the Cli Interaction subcomponent."""

    _valkyrja_abstract = True
