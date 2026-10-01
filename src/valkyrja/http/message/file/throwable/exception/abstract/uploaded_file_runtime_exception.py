#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.http.message.file.throwable.contract.uploaded_file_throwable import (
    UploadedFileThrowable,
)
from valkyrja.http.message.throwable.exception.abstract.http_message_runtime_exception import (
    HttpMessageRuntimeException,
)


class UploadedFileRuntimeException(HttpMessageRuntimeException, UploadedFileThrowable):
    _valkyrja_abstract = True
