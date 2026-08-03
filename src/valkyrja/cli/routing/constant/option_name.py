#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class OptionName:
    """The long name of each option that every command accepts."""

    HELP: Final[str] = "help"
    VERSION: Final[str] = "version"
    QUIET: Final[str] = "quiet"
    SILENT: Final[str] = "silent"
    NO_INTERACTION: Final[str] = "no-interaction"
    TOKEN: Final[str] = "token"
