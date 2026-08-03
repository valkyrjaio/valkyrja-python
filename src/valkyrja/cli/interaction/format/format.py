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


class Format(FormatContract):
    """One ANSI format, with a code that starts it and a code that ends it."""

    def __init__(self, set_code: str, unset_code: str) -> None:
        self._set_code = set_code
        self._unset_code = unset_code

    @override
    def get_set_code(self) -> str:
        return self._set_code

    @override
    def with_set_code(self, set_code: str) -> Self:
        new = copy(self)
        new._set_code = set_code

        return new

    @override
    def get_unset_code(self) -> str:
        return self._unset_code

    @override
    def with_unset_code(self, unset_code: str) -> Self:
        new = copy(self)
        new._unset_code = unset_code

        return new
