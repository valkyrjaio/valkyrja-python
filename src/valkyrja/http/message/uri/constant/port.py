#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final

MIN_PORT: Final[int] = 1
"""The lowest port that TCP and UDP allow."""

MAX_PORT: Final[int] = 65535
"""The highest port that TCP and UDP allow."""


@final
class Port:
    """The port that each scheme uses when a uri names none."""

    HTTP: Final[int] = 80
    HTTPS: Final[int] = 443

    @staticmethod
    def is_valid(port: int) -> bool:
        """Get whether a number is a port that TCP and UDP allow."""
        return MIN_PORT <= port <= MAX_PORT
