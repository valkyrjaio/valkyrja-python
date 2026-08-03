#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum


class SameSite(Enum):
    """Says when a browser sends a cookie with a request from another site."""

    NONE = "none"
    LAX = "lax"
    STRICT = "strict"
