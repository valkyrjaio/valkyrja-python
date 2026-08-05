#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the contracts of the Cli Interaction subcomponent.

The implementation pass fills each contract in. Each test pins that the contract
is abstract, so a later change cannot make it constructible without a failure.
"""

import inspect

import pytest

from valkyrja.cli.interaction.argument.contract.argument_contract import ArgumentContract
from valkyrja.cli.interaction.data.contract.cli_interaction_config_contract import (
    CliInteractionConfigContract,
)
from valkyrja.cli.interaction.format.contract.format_contract import FormatContract
from valkyrja.cli.interaction.formatter.contract.formatter_contract import FormatterContract
from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.message.contract.answer_contract import AnswerContract
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.message.contract.progress_contract import ProgressContract
from valkyrja.cli.interaction.message.contract.question_contract import QuestionContract
from valkyrja.cli.interaction.option.contract.option_contract import OptionContract
from valkyrja.cli.interaction.output.contract.empty_output_contract import EmptyOutputContract
from valkyrja.cli.interaction.output.contract.file_output_contract import FileOutputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.contract.plain_output_contract import PlainOutputContract
from valkyrja.cli.interaction.output.contract.stream_output_contract import StreamOutputContract
from valkyrja.cli.interaction.output.factory.contract.output_factory_contract import (
    OutputFactoryContract,
)
from valkyrja.cli.interaction.writer.contract.writer_contract import WriterContract

CONTRACTS = [
    ArgumentContract,
    OptionContract,
    FormatContract,
    FormatterContract,
    MessageContract,
    AnswerContract,
    ProgressContract,
    QuestionContract,
    WriterContract,
    OutputContract,
    PlainOutputContract,
    EmptyOutputContract,
    StreamOutputContract,
    FileOutputContract,
    OutputFactoryContract,
    InputContract,
    CliInteractionConfigContract,
]

MESSAGE_CONTRACTS = [AnswerContract, ProgressContract, QuestionContract]
OUTPUT_CONTRACTS = [
    PlainOutputContract,
    EmptyOutputContract,
    StreamOutputContract,
    FileOutputContract,
]


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_does_not_construct(contract: type) -> None:
    with pytest.raises(TypeError, match="abstract"):
        contract()


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_declares_an_abstract_method(contract: type) -> None:
    assert inspect.isabstract(contract)


@pytest.mark.parametrize("contract", MESSAGE_CONTRACTS)
def test_a_message_contract_extends_the_message_contract(contract: type) -> None:
    assert issubclass(contract, MessageContract)


@pytest.mark.parametrize("contract", OUTPUT_CONTRACTS)
def test_an_output_contract_extends_the_output_contract(contract: type) -> None:
    assert issubclass(contract, OutputContract)
