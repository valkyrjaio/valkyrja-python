#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Self, override

from valkyrja.http.message.file.enum.upload_error import UploadError
from valkyrja.http.message.file.throwable.exception.abstract.uploaded_file_runtime_exception import (
    UploadedFileRuntimeException,
)

UPLOAD_ERROR_MESSAGES = {
    UploadError.INI_SIZE: "The uploaded file is larger than the size the server allows",
    UploadError.FORM_SIZE: "The uploaded file is larger than the size the form allows",
    UploadError.PARTIAL: "The upload stopped part way through the file",
    UploadError.NO_FILE: "The upload carried no file",
    UploadError.NO_TMP_DIR: "The server holds no directory for an upload",
    UploadError.CANT_WRITE: "The server could not write the upload to a disk",
    UploadError.EXTENSION: "An extension of the server stopped the upload",
}
"""What each upload error tells the user, which PHP keeps in a constant holder."""


class UploadedFileUploadErrorException(UploadedFileRuntimeException):
    def __init__(self, upload_error: UploadError) -> None:
        super().__init__(UPLOAD_ERROR_MESSAGES.get(upload_error, "The upload failed"))

        self._upload_error = upload_error

    def get_upload_error(self) -> UploadError:
        """Get the error that the upload reported."""
        return self._upload_error

    @override
    def __reduce__(self) -> tuple[type[Self], tuple[UploadError]]:
        # `BaseException.__reduce__` replays `args`, and `args` holds the built
        # message, so a copy would build the message from the message itself.
        return type(self), (self._upload_error,)
