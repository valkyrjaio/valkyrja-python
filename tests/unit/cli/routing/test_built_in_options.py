#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the options that every command accepts."""

from collections.abc import Callable

import pytest

from valkyrja.cli.routing.constant.option_name import OptionName
from valkyrja.cli.routing.constant.option_short_name import OptionShortName
from valkyrja.cli.routing.data.contract.option_parameter_contract import (
    OptionParameterContract,
)
from valkyrja.cli.routing.data.option.help_option_parameter import HelpOptionParameter
from valkyrja.cli.routing.data.option.no_interaction_option_parameter import (
    NoInteractionOptionParameter,
)
from valkyrja.cli.routing.data.option.quiet_option_parameter import QuietOptionParameter
from valkyrja.cli.routing.data.option.silent_option_parameter import SilentOptionParameter
from valkyrja.cli.routing.data.option.version_option_parameter import VersionOptionParameter
from valkyrja.cli.routing.enum.option_mode import OptionMode
from valkyrja.cli.routing.enum.option_value_mode import OptionValueMode

BUILT_IN_OPTIONS: list[tuple[Callable[[], OptionParameterContract], str, str]] = [
    (HelpOptionParameter, OptionName.HELP, OptionShortName.HELP),
    (VersionOptionParameter, OptionName.VERSION, OptionShortName.VERSION),
    (QuietOptionParameter, OptionName.QUIET, OptionShortName.QUIET),
    (SilentOptionParameter, OptionName.SILENT, OptionShortName.SILENT),
    (NoInteractionOptionParameter, OptionName.NO_INTERACTION, OptionShortName.NO_INTERACTION),
]


@pytest.mark.parametrize(("option_class", "name", "short_name"), BUILT_IN_OPTIONS)
def test_each_built_in_option_carries_its_names(
    option_class: Callable[[], OptionParameterContract], name: str, short_name: str
) -> None:
    option = option_class()

    assert option.get_name() == name
    assert option.get_short_names() == [short_name]


@pytest.mark.parametrize(("option_class", "name", "short_name"), BUILT_IN_OPTIONS)
def test_each_built_in_option_takes_no_value(
    option_class: Callable[[], OptionParameterContract], name: str, short_name: str
) -> None:
    option = option_class()

    assert option.get_value_mode() is OptionValueMode.NONE
    assert option.get_mode() is OptionMode.OPTIONAL
    assert option.get_description() != ""


def test_the_option_names() -> None:
    assert OptionName.HELP == "help"
    assert OptionName.VERSION == "version"
    assert OptionName.QUIET == "quiet"
    assert OptionName.SILENT == "silent"
    assert OptionName.NO_INTERACTION == "no-interaction"
    assert OptionName.TOKEN == "token"


def test_the_option_short_names() -> None:
    assert OptionShortName.HELP == "h"
    assert OptionShortName.VERSION == "v"
    assert OptionShortName.QUIET == "q"
    assert OptionShortName.SILENT == "s"
    assert OptionShortName.NO_INTERACTION == "N"
    assert OptionShortName.TOKEN == "t"
