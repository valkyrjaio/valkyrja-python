#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.http.message.file.uploaded_file import UploadedFile


@final
class FilelessUploadFixture(UploadedFile):
    """An upload that names neither a file nor a stream, which no constructor allows."""

    def __init__(self) -> None:
        super().__init__(stream=None, file="placeholder")

        self._file = None
