#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Any, Self, override

from valkyrja.cli.interaction.option.contract.option_contract import OptionContract
from valkyrja.cli.routing.data.abstract.parameter import Parameter, ValuedParameter
from valkyrja.cli.routing.data.contract.option_parameter_contract import OptionParameterContract
from valkyrja.cli.routing.enum.option_mode import OptionMode
from valkyrja.cli.routing.enum.option_value_mode import OptionValueMode
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.type.data.cast import Cast


class OptionParameter(Parameter, OptionParameterContract):
    """One named parameter that a command declares."""

    def __init__(
        self,
        name: str,
        description: str = "",
        cast: Cast | None = None,
        short_names: list[str] | None = None,
        mode: OptionMode = OptionMode.OPTIONAL,
        value_mode: OptionValueMode = OptionValueMode.NONE,
        value_display_name: str = "",
        options: list[OptionContract] | None = None,
        container: ContainerContract | None = None,
    ) -> None:
        super().__init__(name, description, cast, container)

        self._short_names: list[str] = list(short_names) if short_names is not None else []
        self._mode = mode
        self._value_mode = value_mode
        self._value_display_name = value_display_name
        self._options: list[OptionContract] = list(options) if options is not None else []

    @override
    def get_short_names(self) -> list[str]:
        return list(self._short_names)

    @override
    def with_short_names(self, *short_names: str) -> Self:
        new = self._copy()
        new._short_names = list(short_names)

        return new

    @override
    def with_added_short_names(self, *short_names: str) -> Self:
        new = self._copy()
        new._short_names = [*new._short_names, *short_names]

        return new

    @override
    def get_mode(self) -> OptionMode:
        return self._mode

    @override
    def with_mode(self, mode: OptionMode) -> Self:
        new = self._copy()
        new._mode = mode

        return new

    @override
    def get_value_mode(self) -> OptionValueMode:
        return self._value_mode

    @override
    def with_value_mode(self, value_mode: OptionValueMode) -> Self:
        new = self._copy()
        new._value_mode = value_mode

        return new

    @override
    def has_value_display_name(self) -> bool:
        return self._value_display_name != ""

    @override
    def get_value_display_name(self) -> str:
        return self._value_display_name

    @override
    def with_value_display_name(self, value_name: str) -> Self:
        new = self._copy()
        new._value_display_name = value_name

        return new

    @override
    def get_options(self) -> list[OptionContract]:
        return list(self._options)

    @override
    def with_options(self, *options: OptionContract) -> Self:
        new = self._copy()
        new._options = list(options)

        return new

    @override
    def with_added_options(self, *options: OptionContract) -> Self:
        new = self._copy()
        new._options = [*new._options, *options]

        return new

    @override
    def get_cast_values(self) -> list[Any]:
        return self._get_cast_values_for_parameters(list[ValuedParameter](self._options))

    @override
    def has_first_value(self) -> bool:
        return self._options != []

    def _copy(self) -> Self:
        """Get a copy that holds its own short name list and option list."""
        new = copy(self)
        new._short_names = list(self._short_names)
        new._options = list(self._options)

        return new
