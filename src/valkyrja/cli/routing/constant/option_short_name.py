#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class OptionShortName:
    """The short name of each option that every command accepts."""

    HELP: Final[str] = "h"
    VERSION: Final[str] = "v"
    QUIET: Final[str] = "q"
    SILENT: Final[str] = "s"
    NO_INTERACTION: Final[str] = "N"
    TOKEN: Final[str] = "t"
