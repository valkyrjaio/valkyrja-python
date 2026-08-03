#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract


class InputHandlerContract(ABC):
    """The contract for the handler that answers one run of the program."""

    @abstractmethod
    def handle(self, input_: InputContract) -> OutputContract:
        """Answer the input, and catch any throwable that the command raises."""

    @abstractmethod
    def exit(self, input_: InputContract, output: OutputContract) -> None:
        """Run the middleware that the process runs as it exits."""

    @abstractmethod
    def run(self, input_: InputContract) -> None:
        """Answer the input, write the output, then end the process."""
