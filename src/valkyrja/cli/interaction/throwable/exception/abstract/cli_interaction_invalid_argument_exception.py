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
from valkyrja.cli.throwable.exception.abstract.cli_invalid_argument_exception import (
    CliInvalidArgumentException,
)


class CliInteractionInvalidArgumentException(CliInvalidArgumentException, CliInteractionThrowable):
    _valkyrja_abstract = True
