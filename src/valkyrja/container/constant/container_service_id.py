#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class ContainerServiceId:
    """The binding key for each service of the Container component.

    A binding key is a string constant, never a class object. A class object as
    a key forces the module of that class to load. TypeScript holds the same
    keys, because both ports resolve a service by string.
    """

    CONTRACT: Final[str] = "Valkyrja.Container.Manager.ContainerContract"
    DATA: Final[str] = "Valkyrja.Container.Data.ContainerData"
