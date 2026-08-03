#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import sys
from typing import override

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.output.contract.empty_output_contract import EmptyOutputContract
from valkyrja.cli.interaction.output.contract.file_output_contract import FileOutputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.contract.plain_output_contract import PlainOutputContract
from valkyrja.cli.interaction.output.contract.stream_output_contract import StreamOutputContract
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.interaction.output.factory.contract.output_factory_contract import (
    OutputFactoryContract,
)
from valkyrja.cli.interaction.output.file_output import FileOutput
from valkyrja.cli.interaction.output.output import Output
from valkyrja.cli.interaction.output.plain_output import PlainOutput
from valkyrja.cli.interaction.output.stream_output import StreamOutput


class OutputFactory(OutputFactoryContract):
    """Builds each kind of output."""

    @override
    def create_output(self, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract) -> OutputContract:
        return Output(True, False, False, exit_code, *messages)

    @override
    def create_empty_output(
        self, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract
    ) -> EmptyOutputContract:
        return EmptyOutput(True, False, False, exit_code, *messages)

    @override
    def create_plain_output(
        self, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract
    ) -> PlainOutputContract:
        return PlainOutput(True, False, False, exit_code, *messages)

    @override
    def create_file_output(
        self, filepath: str, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract
    ) -> FileOutputContract:
        return FileOutput(filepath, True, False, False, exit_code, *messages)

    @override
    def create_stream_output(
        self, exit_code: ExitCode | int = ExitCode.SUCCESS, *messages: MessageContract
    ) -> StreamOutputContract:
        return StreamOutput(sys.stdout, True, False, False, exit_code, *messages)
