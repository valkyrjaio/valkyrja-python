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
    CONTRACT: Final[str] = "valkyrja.container.manager.ContainerContract"
    DATA: Final[str] = "valkyrja.container.data.ContainerData"
