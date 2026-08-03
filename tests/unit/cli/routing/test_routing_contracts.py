#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the contracts and enums of the Cli Routing subcomponent."""

import inspect

import pytest

from valkyrja.cli.routing.data.contract.argument_parameter_contract import (
    ArgumentParameterContract,
)
from valkyrja.cli.routing.data.contract.option_parameter_contract import OptionParameterContract
from valkyrja.cli.routing.data.contract.parameter_contract import ParameterContract
from valkyrja.cli.routing.data.contract.route_contract import RouteContract
from valkyrja.cli.routing.enum.argument_mode import ArgumentMode
from valkyrja.cli.routing.enum.argument_value_mode import ArgumentValueMode
from valkyrja.cli.routing.enum.option_mode import OptionMode
from valkyrja.cli.routing.enum.option_value_mode import OptionValueMode
from valkyrja.cli.routing.provider.contract.cli_route_provider_contract import (
    CliRouteProviderContract,
)

CONTRACTS = [
    ParameterContract,
    ArgumentParameterContract,
    OptionParameterContract,
    RouteContract,
    CliRouteProviderContract,
]


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_does_not_construct(contract: type) -> None:
    with pytest.raises(TypeError, match="abstract"):
        contract()


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_declares_an_abstract_method(contract: type) -> None:
    assert inspect.isabstract(contract)


@pytest.mark.parametrize("contract", [ArgumentParameterContract, OptionParameterContract])
def test_a_parameter_contract_extends_the_parameter_contract(contract: type) -> None:
    assert issubclass(contract, ParameterContract)


def test_argument_mode_members() -> None:
    assert list(ArgumentMode) == [ArgumentMode.REQUIRED, ArgumentMode.OPTIONAL]


def test_argument_value_mode_members() -> None:
    assert list(ArgumentValueMode) == [ArgumentValueMode.DEFAULT, ArgumentValueMode.ARRAY]


def test_option_mode_members() -> None:
    assert list(OptionMode) == [OptionMode.REQUIRED, OptionMode.OPTIONAL]


def test_option_value_mode_members() -> None:
    assert list(OptionValueMode) == [
        OptionValueMode.NONE,
        OptionValueMode.DEFAULT,
        OptionValueMode.ARRAY,
    ]
