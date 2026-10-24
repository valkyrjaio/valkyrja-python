#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.http.message.file.contract.uploaded_file_contract import UploadedFileContract


class UploadedFileCollectionContract(ABC):
    @abstractmethod
    def has(self, key: str) -> bool:
        """Get whether the collection holds an upload under a given key."""

    @abstractmethod
    def get(self, key: str) -> UploadedFileContract:
        """Get the upload under a given key."""

    @abstractmethod
    def get_all(self) -> dict[str, UploadedFileContract]:
        """Get every upload."""

    @abstractmethod
    def with_file(self, key: str, file: UploadedFileContract) -> Self:
        """Get a copy of the collection that holds one more upload."""

    @abstractmethod
    def without_file(self, key: str) -> Self:
        """Get a copy of the collection that holds one fewer upload."""
