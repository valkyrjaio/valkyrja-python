#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the concrete exceptions of the Cli Interaction subcomponent."""

import pytest

from valkyrja.cli.interaction.throwable.contract.cli_interaction_throwable import (
    CliInteractionThrowable,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_expected_question_output_exception import (
    CliInteractionExpectedQuestionOutputException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_invalid_empty_value_exception import (
    CliInteractionInvalidEmptyValueException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_invalid_non_empty_value_exception import (
    CliInteractionInvalidNonEmptyValueException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_invalid_option_name_exception import (
    CliInteractionInvalidOptionNameException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_no_formatter_exception import (
    CliInteractionNoFormatterException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_no_validation_callable_exception import (
    CliInteractionNoValidationCallableException,
)

RUNTIME_EXCEPTIONS: list[type] = [
    CliInteractionNoFormatterException,
    CliInteractionNoValidationCallableException,
    CliInteractionExpectedQuestionOutputException,
]
INVALID_ARGUMENT_EXCEPTIONS: list[type] = [
    CliInteractionInvalidOptionNameException,
    CliInteractionInvalidEmptyValueException,
    CliInteractionInvalidNonEmptyValueException,
]


@pytest.mark.parametrize("exception_class", RUNTIME_EXCEPTIONS + INVALID_ARGUMENT_EXCEPTIONS)
def test_a_concrete_exception_constructs_and_carries_its_message(exception_class: type) -> None:
    exception = exception_class("Custom message")

    assert str(exception) == "Custom message"
    assert isinstance(exception, CliInteractionThrowable)


@pytest.mark.parametrize("exception_class", RUNTIME_EXCEPTIONS)
def test_a_runtime_exception_extends_the_language_root(exception_class: type) -> None:
    assert issubclass(exception_class, RuntimeError)


@pytest.mark.parametrize("exception_class", INVALID_ARGUMENT_EXCEPTIONS)
def test_an_invalid_argument_exception_extends_the_language_root(exception_class: type) -> None:
    assert issubclass(exception_class, ValueError)


@pytest.mark.parametrize("exception_class", RUNTIME_EXCEPTIONS + INVALID_ARGUMENT_EXCEPTIONS)
def test_a_concrete_exception_gets_a_trace_code(exception_class: type) -> None:
    assert exception_class("Custom message").get_trace_code()
