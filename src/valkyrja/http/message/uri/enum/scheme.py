#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum


class Scheme(Enum):
    """The scheme that a uri carries."""

    EMPTY = ""
    HTTP = "http"
    HTTPS = "https"
