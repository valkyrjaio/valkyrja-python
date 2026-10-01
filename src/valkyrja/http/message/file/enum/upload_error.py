#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import IntEnum


class UploadError(IntEnum):
    OK = 0
    INI_SIZE = 1
    FORM_SIZE = 2
    PARTIAL = 3
    NO_FILE = 4
    NO_TMP_DIR = 6
    CANT_WRITE = 7
    EXTENSION = 8
