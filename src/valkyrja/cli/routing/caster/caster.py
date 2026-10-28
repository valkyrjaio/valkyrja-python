#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, final, override
from typing import cast as type_cast

from valkyrja.cli.routing.caster.contract.caster_contract import CasterContract
from valkyrja.cli.routing.data.contract.parameter_contract import ParameterContract
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.type.constant.cast_argument import CastArgument
from valkyrja.type.contract.type_contract import TypeContract


@final
class Caster(CasterContract):
    def __init__(self, container: ContainerContract) -> None:
        self._container = container

    @override
    def get_cast_values(self, parameter: ParameterContract) -> list[Any]:
        values = parameter.get_values()

        if not parameter.has_cast():
            return list(values)

        cast = parameter.get_cast()
        cast_values: list[Any] = []

        for value in values:
            # PHP writes `$castType::fromValue($value)`, a static call on a variable
            # class, which Python cannot make. The cast names a binding key instead.
            # The ask is for a service, never a singleton: a singleton would build one
            # type from an empty argument map and answer with it for every value.
            type_ = type_cast("TypeContract", self._container.get_service(cast.type_, {CastArgument.VALUE: value}))

            cast_values.append(type_.as_value() if cast.convert else type_)

        return cast_values
