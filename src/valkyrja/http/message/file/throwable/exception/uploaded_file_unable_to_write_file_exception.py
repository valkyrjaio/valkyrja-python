#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.file.throwable.exception.abstract.uploaded_file_runtime_exception import (
    UploadedFileRuntimeException,
)


class UploadedFileUnableToWriteFileException(UploadedFileRuntimeException):
    pass
