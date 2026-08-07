#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class ThrowableServiceId:
    """The binding key for each service of the Throwable component.

    A binding key is a string constant, never a class object. A class object as
    a key forces the module of that class to load.

    The key is the import path of the module, with the `Contract` segment
    removed. A port never copies a key from another port, because each port has
    its own directory layout.
    """

    HANDLER_CONTRACT: Final[str] = "valkyrja.throwable.handler.ThrowableHandlerContract"
