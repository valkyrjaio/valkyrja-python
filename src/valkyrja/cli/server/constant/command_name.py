#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class CommandName:
    """The name of each command that the framework ships."""

    HELP: Final[str] = "help"
    LIST: Final[str] = "list"
    LIST_BASH: Final[str] = "list:bash"
    VERSION: Final[str] = "version"
    DATA_GENERATE: Final[str] = "data:generate"
