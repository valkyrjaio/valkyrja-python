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
from valkyrja.cli.interaction.throwable.exception.cli_interaction_file_write_exception import (
    CliInteractionFileWriteException,
)


class FileOutput(Output, FileOutputContract):
    def __init__(
        self,
        filepath: str,
        *messages: MessageContract,
        is_interactive: bool = True,
        is_quiet: bool = False,
        is_silent: bool = False,
        exit_code: ExitCode | int = ExitCode.SUCCESS,
    ) -> None:
        super().__init__(
            *messages,
            is_interactive=is_interactive,
            is_quiet=is_quiet,
            is_silent=is_silent,
            exit_code=exit_code,
        )

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
        data = message.get_formatted_text()

        try:
            with open(self._filepath, "a", encoding="utf-8") as file:
                written = file.write(data)
        except OSError as exception:
            raise CliInteractionFileWriteException(
                f"Unable to write the whole message to the file `{self._filepath}`: {exception}"
            ) from exception

        if written != len(data):
            raise CliInteractionFileWriteException(
                f"Unable to write the whole message to the file `{self._filepath}`: "
                f"the write stored {written} of {len(data)} characters"
            )
