#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum


class ProtocolVersion(Enum):
    """The version of HTTP that a message speaks."""

    V1 = "1.0"
    V1_1 = "1.1"
    V2 = "2"
    V3 = "3"
