#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.http.message.file.enum.upload_error import UploadError
from valkyrja.http.message.stream.contract.stream_contract import StreamContract


class UploadedFileContract(ABC):
    @abstractmethod
    def get_stream(self) -> StreamContract:
        """Get the stream that holds the upload."""

    @abstractmethod
    def move_to(self, target_path: str) -> None:
        """Move the upload to one path, which it does once."""

    @abstractmethod
    def has_size(self) -> bool:
        """Get whether the upload reports a size."""

    @abstractmethod
    def get_size(self) -> int:
        """Get how many bytes the upload holds."""

    @abstractmethod
    def get_error(self) -> UploadError:
        """Get what the upload reports about itself."""

    @abstractmethod
    def has_client_filename(self) -> bool:
        """Get whether the client named the file."""

    @abstractmethod
    def get_client_filename(self) -> str:
        """Get the name that the client gave the file."""

    @abstractmethod
    def has_client_media_type(self) -> bool:
        """Get whether the client named the media type."""

    @abstractmethod
    def get_client_media_type(self) -> str:
        """Get the media type that the client gave the file."""
