#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class CliInteractionServiceId:
    INPUT_CONTRACT: Final[str] = "valkyrja.cli.interaction.input.InputContract"
    OUTPUT_CONTRACT: Final[str] = "valkyrja.cli.interaction.output.OutputContract"
    OUTPUT_FACTORY_CONTRACT: Final[str] = "valkyrja.cli.interaction.output.factory.OutputFactoryContract"
    CONFIG_CONTRACT: Final[str] = "valkyrja.cli.interaction.data.CliInteractionConfigContract"
