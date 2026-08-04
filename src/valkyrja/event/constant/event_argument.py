#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class EventArgument:
    """The key that the dispatcher files an event under, in the arguments of a handler."""

    EVENT: Final[str] = "event"
