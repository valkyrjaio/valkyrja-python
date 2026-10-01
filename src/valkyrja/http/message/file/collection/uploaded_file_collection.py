#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.file.collection.contract.uploaded_file_collection_contract import (
    UploadedFileCollectionContract,
)
from valkyrja.http.message.file.contract.uploaded_file_contract import UploadedFileContract
from valkyrja.http.message.file.throwable.exception.uploaded_file_invalid_key_exception import (
    UploadedFileInvalidKeyException,
)


class UploadedFileCollection(UploadedFileCollectionContract):
    def __init__(self, files: dict[str, UploadedFileContract] | None = None) -> None:
        self._files: dict[str, UploadedFileContract] = dict(files) if files is not None else {}

    @override
    def has(self, key: str) -> bool:
        return key in self._files

    @override
    def get(self, key: str) -> UploadedFileContract:
        file = self._files.get(key)

        if file is None:
            raise UploadedFileInvalidKeyException(f"Uploaded file {key} does not exist")

        return file

    @override
    def get_all(self) -> dict[str, UploadedFileContract]:
        return dict(self._files)

    @override
    def with_file(self, key: str, file: UploadedFileContract) -> Self:
        new = self._copy()
        new._files[key] = file

        return new

    @override
    def without_file(self, key: str) -> Self:
        new = self._copy()
        new._files.pop(key, None)

        return new

    def _copy(self) -> Self:
        """Get a copy that holds its own map of uploads."""
        new = copy(self)
        new._files = dict(self._files)

        return new
