#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import IntEnum


class ExitCode(IntEnum):
    """The code that a command gives back to the shell.

    The values follow the `sysexits.h` convention, so a shell reads a failure
    the way it reads a failure of any other program.
    """

    SUCCESS = 0
    ERROR = 1

    USAGE_ERROR = 64
    DATA_ERROR = 65
    NO_INPUT = 67
    NO_USER = 68
    UNAVAILABLE = 69
    SOFTWARE_ERROR = 70
    OS_ERROR = 71
    OS_FILE_ERROR = 72
    CANT_CREATE = 73
    IO_ERROR = 74
    TEMP_FAIL = 75
    PROTOCOL_ERROR = 76
    NO_PERMISSION = 77
    CONFIG_ERROR = 78

    AUTO_EXIT = 255
