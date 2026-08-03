#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self, TextIO

from valkyrja.cli.interaction.output.contract.output_contract import OutputContract


class StreamOutputContract(OutputContract):
    """The contract for an output that writes to a stream.

    PHP holds a resource. Python holds a `TextIO`, which is what `open` and
    `sys.stdout` both give.
    """

    @abstractmethod
    def get_stream(self) -> TextIO:
        """Get the stream that the output writes to."""

    @abstractmethod
    def with_stream(self, stream: TextIO) -> Self:
        """Get a copy of the output that writes to a different stream."""
