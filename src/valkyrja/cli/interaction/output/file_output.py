#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.output.contract.file_output_contract import FileOutputContract
from valkyrja.cli.interaction.output.output import Output


class FileOutput(Output, FileOutputContract):
    """An output that appends each message to a file."""

    def __init__(
        self,
        filepath: str,
        is_interactive: bool = True,
        is_quiet: bool = False,
        is_silent: bool = False,
        exit_code: ExitCode | int = ExitCode.SUCCESS,
        *messages: MessageContract,
    ) -> None:
        super().__init__(is_interactive, is_quiet, is_silent, exit_code, *messages)

        self._filepath = filepath

    @override
    def get_filepath(self) -> str:
        return self._filepath

    @override
    def with_filepath(self, filepath: str) -> Self:
        new = copy(self)
        new._filepath = filepath

        return new

    @override
    def _output_message(self, message: MessageContract) -> None:
        with open(self._filepath, "a", encoding="utf-8") as file:
            file.write(message.get_formatted_text())
