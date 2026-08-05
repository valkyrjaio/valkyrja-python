#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the middleware that the Cli Server ships."""

import pytest

from valkyrja.cli.interaction.data.cli_interaction_config import CliInteractionConfig
from valkyrja.cli.interaction.input.input import Input
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.option.option import Option
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.middleware.handler.input_received_handler import InputReceivedHandler
from valkyrja.cli.middleware.handler.throwable_caught_handler import ThrowableCaughtHandler
from valkyrja.cli.routing.constant.option_name import OptionName
from valkyrja.cli.routing.constant.option_short_name import OptionShortName
from valkyrja.cli.server.constant.command_name import CommandName
from valkyrja.cli.server.middleware.input_received.check_for_help_options_middleware import (
    CheckForHelpOptionsMiddleware,
)
from valkyrja.cli.server.middleware.input_received.check_for_version_options_middleware import (
    CheckForVersionOptionsMiddleware,
)
from valkyrja.cli.server.middleware.input_received.check_global_interaction_options_middleware import (
    CheckGlobalInteractionOptionsMiddleware,
)
from valkyrja.cli.server.middleware.throwable_caught.output_throwable_caught_middleware import (
    OutputThrowableCaughtMiddleware,
)
from valkyrja.container.manager.container import Container


def make_interaction_middleware(
    config: CliInteractionConfig,
) -> CheckGlobalInteractionOptionsMiddleware:
    return CheckGlobalInteractionOptionsMiddleware(
        config=config,
        no_interaction_option_name=OptionName.NO_INTERACTION,
        no_interaction_option_short_name=OptionShortName.NO_INTERACTION,
        quiet_option_name=OptionName.QUIET,
        quiet_option_short_name=OptionShortName.QUIET,
        silent_option_name=OptionName.SILENT,
        silent_option_short_name=OptionShortName.SILENT,
    )


@pytest.mark.parametrize(
    ("middleware_class", "command_name", "option_name", "short_name"),
    [
        (CheckForHelpOptionsMiddleware, CommandName.HELP, OptionName.HELP, OptionShortName.HELP),
        (
            CheckForVersionOptionsMiddleware,
            CommandName.VERSION,
            OptionName.VERSION,
            OptionShortName.VERSION,
        ),
    ],
)
def test_the_option_sends_the_input_to_its_command(
    middleware_class: type, command_name: str, option_name: str, short_name: str
) -> None:
    middleware = middleware_class(command_name, option_name, short_name)
    handler = InputReceivedHandler(Container())
    input_ = Input(command_name="run", options=[Option(option_name)])

    answered = middleware.input_received(input_, handler)

    assert answered.get_command_name() == command_name
    assert answered.get_options() == []


@pytest.mark.parametrize(
    ("middleware_class", "command_name", "option_name", "short_name"),
    [
        (CheckForHelpOptionsMiddleware, CommandName.HELP, OptionName.HELP, OptionShortName.HELP),
        (
            CheckForVersionOptionsMiddleware,
            CommandName.VERSION,
            OptionName.VERSION,
            OptionShortName.VERSION,
        ),
    ],
)
def test_the_short_option_sends_the_input_to_its_command(
    middleware_class: type, command_name: str, option_name: str, short_name: str
) -> None:
    middleware = middleware_class(command_name, option_name, short_name)
    input_ = Input(command_name="run", options=[Option(short_name)])

    answered = middleware.input_received(input_, InputReceivedHandler(Container()))

    assert answered.get_command_name() == command_name


@pytest.mark.parametrize(
    ("middleware_class", "command_name", "option_name", "short_name"),
    [
        (CheckForHelpOptionsMiddleware, CommandName.HELP, OptionName.HELP, OptionShortName.HELP),
        (
            CheckForVersionOptionsMiddleware,
            CommandName.VERSION,
            OptionName.VERSION,
            OptionShortName.VERSION,
        ),
    ],
)
def test_the_input_passes_through_without_the_option(
    middleware_class: type, command_name: str, option_name: str, short_name: str
) -> None:
    middleware = middleware_class(command_name, option_name, short_name)
    input_ = Input(command_name="run")

    assert middleware.input_received(input_, InputReceivedHandler(Container())) is input_


def test_the_no_interaction_option_stops_a_question() -> None:
    config = CliInteractionConfig()
    middleware = make_interaction_middleware(config)

    middleware.input_received(Input(options=[Option(OptionName.NO_INTERACTION)]), InputReceivedHandler(Container()))

    assert not config.is_interactive


def test_the_quiet_option_drops_a_message() -> None:
    config = CliInteractionConfig()

    make_interaction_middleware(config).input_received(
        Input(options=[Option(OptionShortName.QUIET)]), InputReceivedHandler(Container())
    )

    assert config.is_quiet


def test_the_silent_option_writes_nothing() -> None:
    config = CliInteractionConfig()

    make_interaction_middleware(config).input_received(
        Input(options=[Option(OptionName.SILENT)]), InputReceivedHandler(Container())
    )

    assert config.is_silent


def test_the_config_keeps_its_defaults_without_an_option() -> None:
    config = CliInteractionConfig()

    make_interaction_middleware(config).input_received(Input(), InputReceivedHandler(Container()))

    assert config.is_interactive
    assert not config.is_quiet
    assert not config.is_silent


def test_the_throwable_middleware_writes_the_output() -> None:
    output = EmptyOutput(True, False, False).with_added_message(Message("boom"))

    written = OutputThrowableCaughtMiddleware().throwable_caught(
        Input(), output, RuntimeError("boom"), ThrowableCaughtHandler(Container())
    )

    assert written.has_written_message()


def test_the_command_names() -> None:
    assert CommandName.HELP == "help"
    assert CommandName.LIST == "list"
    assert CommandName.LIST_BASH == "list:bash"
    assert CommandName.VERSION == "version"
    assert CommandName.DATA_GENERATE == "data:generate"
