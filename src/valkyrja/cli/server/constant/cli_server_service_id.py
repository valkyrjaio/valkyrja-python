#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class CliServerServiceId:
    """The binding key for each service of the Cli Server subcomponent.

    The input and the output keys belong to `CliInteractionServiceId`, which
    owns those services. A second copy of a key here would drift from the first.
    """

    INPUT_HANDLER_CONTRACT: Final[str] = "Valkyrja.Cli.Server.Handler.InputHandlerContract"
