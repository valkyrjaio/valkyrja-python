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
    """The binding key for each service of the Cli Interaction subcomponent.

    A binding key is a string constant, never a class object. A class object as
    a key forces the module of that class to load.

    The key is the import path of the module, with the `Contract` segment
    removed. A port never copies a key from another port, because each port has
    its own directory layout.
    """

    INPUT_CONTRACT: Final[str] = "valkyrja.cli.interaction.input.InputContract"
    OUTPUT_CONTRACT: Final[str] = "valkyrja.cli.interaction.output.OutputContract"
    OUTPUT_FACTORY_CONTRACT: Final[str] = "valkyrja.cli.interaction.output.factory.OutputFactoryContract"
    CONFIG_CONTRACT: Final[str] = "valkyrja.cli.interaction.data.CliInteractionConfigContract"
