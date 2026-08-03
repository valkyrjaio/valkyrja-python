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
    a key forces the module of that class to load. TypeScript holds the same
    keys, because both ports resolve a service by string.
    """

    INPUT_CONTRACT: Final[str] = "Valkyrja.Cli.Interaction.Input.InputContract"
    OUTPUT_CONTRACT: Final[str] = "Valkyrja.Cli.Interaction.Output.OutputContract"
    OUTPUT_FACTORY_CONTRACT: Final[str] = "Valkyrja.Cli.Interaction.Output.Factory.OutputFactoryContract"
    CONFIG_CONTRACT: Final[str] = "Valkyrja.Cli.Interaction.Data.CliInteractionConfigContract"
