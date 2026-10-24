#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from pathlib import Path
from typing import override

from valkyrja.http.message.file.contract.uploaded_file_contract import UploadedFileContract
from valkyrja.http.message.file.enum.upload_error import UploadError
from valkyrja.http.message.file.throwable.exception.uploaded_file_already_moved_exception import (
    UploadedFileAlreadyMovedException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_invalid_directory_exception import (
    UploadedFileInvalidDirectoryException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_invalid_uploaded_file_exception import (
    UploadedFileInvalidUploadedFileException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_unable_to_write_file_exception import (
    UploadedFileUnableToWriteFileException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_upload_error_exception import (
    UploadedFileUploadErrorException,
)
from valkyrja.http.message.stream.contract.stream_contract import StreamContract
from valkyrja.http.message.stream.enum.mode import Mode
from valkyrja.http.message.stream.stream import Stream


class UploadedFile(UploadedFileContract):
    def __init__(
        self,
        file: str | None = None,
        stream: StreamContract | None = None,
        upload_error: UploadError = UploadError.OK,
        size: int = 0,
        file_name: str = "",
        media_type: str = "",
    ) -> None:
        if upload_error is UploadError.OK and file is None and stream is None:
            raise UploadedFileInvalidUploadedFileException("One of file or stream are required")

        self._file = file
        self._stream = stream
        self._upload_error = upload_error
        self._size = size
        self._file_name = file_name
        self._media_type = media_type
        self._has_been_moved = False

    @override
    def get_stream(self) -> StreamContract:
        self._validate_no_upload_error()
        self._validate_has_not_been_moved("Cannot retrieve stream after it has already been moved")

        if self._stream is not None:
            return self._stream

        # The constructor refuses an upload that names neither, so this guard holds
        # only for a subclass that replaces it.
        if self._file is None:
            raise UploadedFileInvalidUploadedFileException("One of file or stream are required")

        # The mode is read. A write mode would truncate the upload that this stream
        # exists to read.
        self._stream = Stream(self._file, Mode.READ)

        return self._stream

    @override
    def move_to(self, target_path: str) -> None:
        self._validate_no_upload_error()
        self._validate_has_not_been_moved()
        self._validate_target_directory(str(Path(target_path).parent))
        self._write_stream(target_path)

        self._has_been_moved = True

    @override
    def has_size(self) -> bool:
        return self._size != 0

    @override
    def get_size(self) -> int:
        return self._size

    @override
    def get_error(self) -> UploadError:
        return self._upload_error

    @override
    def has_client_filename(self) -> bool:
        return self._file_name != ""

    @override
    def get_client_filename(self) -> str:
        return self._file_name

    @override
    def has_client_media_type(self) -> bool:
        return self._media_type != ""

    @override
    def get_client_media_type(self) -> str:
        return self._media_type

    def _validate_no_upload_error(self) -> None:
        """Refuse an upload that reports a failure of its own."""
        if self._upload_error is not UploadError.OK:
            raise UploadedFileUploadErrorException(self._upload_error)

    def _validate_has_not_been_moved(self, message: str = "Cannot move file after it has already been moved") -> None:
        """Refuse a second move, which PSR-7 does not allow."""
        if self._has_been_moved:
            raise UploadedFileAlreadyMovedException(message)

    @staticmethod
    def _validate_target_directory(target_directory: str) -> None:
        """Refuse a directory that holds no file, or that takes no write."""
        directory = Path(target_directory)

        if not directory.is_dir():
            raise UploadedFileInvalidDirectoryException(
                f"The target directory `{target_directory}` does not exists or is not writable"
            )

    def _write_stream(self, target_path: str) -> None:
        """Write the upload to the path, and close the stream it came from."""
        stream = self.get_stream()
        stream.rewind()

        try:
            with Path(target_path).open("wb") as target:
                target.write(stream.get_contents())
        except OSError as exception:
            raise UploadedFileUnableToWriteFileException(
                f"Unable to write the upload to `{target_path}`"
            ) from exception

        stream.close()
