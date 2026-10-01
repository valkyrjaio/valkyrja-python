#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class Char:
    UNRESERVED: Final[str] = r"a-zA-Z0-9_\-\.~"
    SUB_DELIMS: Final[str] = r"!\$&'\(\)\*\+,;="
    USER_INFO: Final[str] = UNRESERVED + SUB_DELIMS + ":"
    HOST: Final[str] = UNRESERVED + SUB_DELIMS
    PATH: Final[str] = UNRESERVED + SUB_DELIMS + r":@\/"
    QUERY: Final[str] = UNRESERVED + SUB_DELIMS + r":@\/\?"
