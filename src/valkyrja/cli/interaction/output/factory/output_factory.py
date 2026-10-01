#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import TextIO, override

from valkyrja.cli.interaction.data.cli_interaction_config import CliInteractionConfig
from valkyrja.cli.interaction.data.contract.cli_interaction_config_contract import (
    CliInteractionConfigContract,
)
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
    def __init__(self, config: CliInteractionConfigContract | None = None) -> None:
        # Warning: the default config is built here, never in the signature. Python
        # builds a default argument once, at import, so every factory would share one
        # config, and a write to that config would reach each of them.
        self._config = config if config is not None else CliInteractionConfig()

    @override
    def create_output(self, *messages: MessageContract, exit_code: ExitCode | int = ExitCode.SUCCESS) -> OutputContract:
        return Output(*messages, **self._flags(), exit_code=exit_code)

    @override
    def create_empty_output(
        self, *messages: MessageContract, exit_code: ExitCode | int = ExitCode.SUCCESS
    ) -> EmptyOutputContract:
        return EmptyOutput(*messages, **self._flags(), exit_code=exit_code)

    @override
    def create_plain_output(
        self, *messages: MessageContract, exit_code: ExitCode | int = ExitCode.SUCCESS
    ) -> PlainOutputContract:
        return PlainOutput(*messages, **self._flags(), exit_code=exit_code)

    @override
    def create_file_output(
        self, filepath: str, *messages: MessageContract, exit_code: ExitCode | int = ExitCode.SUCCESS
    ) -> FileOutputContract:
        return FileOutput(filepath, *messages, **self._flags(), exit_code=exit_code)

    @override
    def create_stream_output(
        self, stream: TextIO, *messages: MessageContract, exit_code: ExitCode | int = ExitCode.SUCCESS
    ) -> StreamOutputContract:
        return StreamOutput(stream, *messages, **self._flags(), exit_code=exit_code)

    def _flags(self) -> dict[str, bool]:
        """Read the three flags that every output carries from the config."""
        return {
            "is_interactive": self._config.is_interactive,
            "is_quiet": self._config.is_quiet,
            "is_silent": self._config.is_silent,
        }
