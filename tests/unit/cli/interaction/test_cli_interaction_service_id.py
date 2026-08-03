#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for CliInteractionServiceId.

Each key is part of the public API, so each test pins the whole string.
"""

from valkyrja.cli.interaction.constant.cli_interaction_service_id import CliInteractionServiceId


def test_input_contract() -> None:
    assert CliInteractionServiceId.INPUT_CONTRACT == "Valkyrja.Cli.Interaction.Input.InputContract"


def test_output_contract() -> None:
    assert CliInteractionServiceId.OUTPUT_CONTRACT == "Valkyrja.Cli.Interaction.Output.OutputContract"


def test_output_factory_contract() -> None:
    assert (
        CliInteractionServiceId.OUTPUT_FACTORY_CONTRACT
        == "Valkyrja.Cli.Interaction.Output.Factory.OutputFactoryContract"
    )


def test_config_contract() -> None:
    assert CliInteractionServiceId.CONFIG_CONTRACT == "Valkyrja.Cli.Interaction.Data.CliInteractionConfigContract"
