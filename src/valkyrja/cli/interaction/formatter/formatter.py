#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.cli.interaction.format.contract.format_contract import FormatContract
from valkyrja.cli.interaction.formatter.contract.formatter_contract import FormatterContract


class Formatter(FormatterContract):
    """Puts each format around a text with an ANSI escape sequence."""

    def __init__(self, *formats: FormatContract) -> None:
        self._formats: list[FormatContract] = list(formats)

    @override
    def get_formats(self) -> list[FormatContract]:
        return list(self._formats)

    @override
    def with_formats(self, *formats: FormatContract) -> Self:
        new = copy(self)
        new._formats = list(formats)

        return new

    @override
    def format_text(self, text: str) -> str:
        if not self._formats:
            return text

        set_codes = ";".join(format_.get_set_code() for format_ in self._formats)
        unset_codes = ";".join(format_.get_unset_code() for format_ in self._formats)

        return f"\033[{set_codes}m{text}\033[{unset_codes}m"
