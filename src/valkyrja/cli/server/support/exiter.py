#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import sys
from typing import final


@final
class Exiter:
    """Ends the process with the code that a command gave.

    A test freezes the exiter, because a test cannot end the process that runs
    it. PHP holds the same seam for the same reason.
    """

    _exit = True

    @staticmethod
    def freeze() -> None:
        """Stop the exiter from ending the process."""
        Exiter._exit = False

    @staticmethod
    def unfreeze() -> None:
        """Let the exiter end the process again."""
        Exiter._exit = True

    @staticmethod
    def is_frozen() -> bool:
        """Get whether the exiter ends the process."""
        return not Exiter._exit

    @staticmethod
    def exit(code: int = 0) -> None:
        """End the process, unless a test froze the exiter."""
        if Exiter._exit:
            sys.exit(code)
