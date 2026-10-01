#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Self, final, override

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.input.input import Input
from valkyrja.cli.interaction.output.empty_output import EmptyOutput


@final
class UnwritableOutputFixture(EmptyOutput):
    """An output whose write reports a failure of its destination."""

    @override
    def write_messages(self) -> Self:
        raise RuntimeError("the destination refused the write")


@final
class CodelessOutputFixture(EmptyOutput):
    """An output that raises on the read of its exit code."""

    @override
    def get_exit_code(self) -> ExitCode | int:
        raise RuntimeError("the exit code is unreadable")


@final
class NamelessInputFixture(Input):
    """An input that raises on the read of its command name."""

    @override
    def get_command_name(self) -> str:
        raise RuntimeError("the command name is unreadable")
