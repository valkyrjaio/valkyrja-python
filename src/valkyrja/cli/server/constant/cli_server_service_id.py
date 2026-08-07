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
    INPUT_HANDLER_CONTRACT: Final[str] = "valkyrja.cli.server.handler.InputHandlerContract"
