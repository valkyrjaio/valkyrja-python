#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.cli.interaction.formatter.contract.formatter_contract import FormatterContract
from valkyrja.cli.interaction.message.contract.progress_contract import ProgressContract
from valkyrja.cli.interaction.message.message import Message


class Progress(Message, ProgressContract):
    """A message that reports how far a task has run."""

    def __init__(
        self,
        text: str,
        is_complete: bool = False,
        percentage: int = 0,
        formatter: FormatterContract | None = None,
    ) -> None:
        super().__init__(text, formatter)

        self._is_complete = is_complete
        self._percentage = percentage

    @override
    def is_complete(self) -> bool:
        return self._is_complete

    @override
    def with_is_complete(self, is_complete: bool) -> Self:
        new = copy(self)
        new._is_complete = is_complete

        return new

    @override
    def get_percentage(self) -> int:
        return self._percentage

    @override
    def with_percentage(self, percentage: int) -> Self:
        new = copy(self)
        new._percentage = percentage

        return new
