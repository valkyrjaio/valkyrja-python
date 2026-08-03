#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self

from valkyrja.cli.interaction.output.contract.output_contract import OutputContract


class FileOutputContract(OutputContract):
    """The contract for an output that writes to a file."""

    @abstractmethod
    def get_filepath(self) -> str:
        """Get the path of the file that the output writes to."""

    @abstractmethod
    def with_filepath(self, filepath: str) -> Self:
        """Get a copy of the output that writes to a different file."""
