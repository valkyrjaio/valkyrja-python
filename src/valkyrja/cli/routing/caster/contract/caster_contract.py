#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Any

from valkyrja.cli.routing.data.contract.parameter_contract import ParameterContract


class CasterContract(ABC):
    @abstractmethod
    def get_cast_values(self, parameter: ParameterContract) -> list[Any]:
        """Get each value of the parameter, with the cast of the parameter applied."""
