#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum, auto


class InvalidReferenceMode(Enum):
    """What the container does when it has no service for an id."""

    NEW_INSTANCE_OR_THROW_EXCEPTION = auto()
    """Construct the service, or raise an exception when construction fails."""

    THROW_EXCEPTION = auto()
    """Raise an exception."""
