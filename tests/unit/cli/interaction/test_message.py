#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the messages."""

import pytest

from valkyrja.cli.interaction.enum.text_color import TextColor
from valkyrja.cli.interaction.format.text_color_format import TextColorFormat
from valkyrja.cli.interaction.formatter.formatter import Formatter
from valkyrja.cli.interaction.message.banner import Banner
from valkyrja.cli.interaction.message.error_message import ErrorMessage
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.message.messages import Messages
from valkyrja.cli.interaction.message.new_line import NewLine
from valkyrja.cli.interaction.message.success_message import SuccessMessage
from valkyrja.cli.interaction.message.warning_message import WarningMessage
from valkyrja.cli.interaction.throwable.exception.cli_interaction_no_formatter_exception import (
    CliInteractionNoFormatterException,
)


def test_a_message_holds_its_text() -> None:
    assert Message("hello").get_text() == "hello"


def test_a_message_with_no_formatter_returns_the_text() -> None:
    assert Message("hello").get_formatted_text() == "hello"


def test_a_message_with_a_formatter_formats_the_text() -> None:
    message = Message("hello", Formatter(TextColorFormat(TextColor.RED)))

    assert message.get_formatted_text() == "\033[31mhello\033[39m"


def test_has_formatter() -> None:
    assert not Message("hello").has_formatter()
    assert Message("hello", Formatter()).has_formatter()


def test_get_formatter_raises_without_one() -> None:
    with pytest.raises(CliInteractionNoFormatterException, match="No formatter has been set"):
        Message("hello").get_formatter()


def test_get_formatter_returns_the_formatter() -> None:
    formatter = Formatter()

    assert Message("hello", formatter).get_formatter() is formatter


def test_with_text_returns_a_copy() -> None:
    message = Message("hello")

    changed = message.with_text("goodbye")

    assert changed is not message
    assert changed.get_text() == "goodbye"
    assert message.get_text() == "hello"


def test_with_formatter_returns_a_copy() -> None:
    message = Message("hello")
    formatter = Formatter()

    changed = message.with_formatter(formatter)

    assert changed is not message
    assert changed.get_formatter() is formatter
    assert not message.has_formatter()


def test_without_formatter_returns_a_copy() -> None:
    message = Message("hello", Formatter())

    changed = message.without_formatter()

    assert changed is not message
    assert not changed.has_formatter()
    assert message.has_formatter()


@pytest.mark.parametrize("message_class", [ErrorMessage, SuccessMessage, WarningMessage])
def test_each_named_message_carries_a_formatter(message_class: type[Message]) -> None:
    message = message_class("problem")

    assert message.get_text() == "problem"
    assert message.has_formatter()
    assert message.get_formatted_text() != "problem"


def test_a_new_line_holds_a_line_break() -> None:
    assert NewLine().get_text() == "\n"


def test_a_new_line_takes_a_formatter() -> None:
    assert NewLine(Formatter(TextColorFormat(TextColor.RED))).get_formatted_text() != "\n"


def test_messages_joins_the_text_of_each_message() -> None:
    messages = Messages(Message("a"), Message("b"), NewLine())

    assert messages.get_text() == "ab\n"


def test_messages_joins_the_formatted_text_of_each_message() -> None:
    messages = Messages(Message("a", Formatter(TextColorFormat(TextColor.RED))), Message("b"))

    assert messages.get_formatted_text() == "\033[31ma\033[39mb"


def test_messages_with_none_is_empty() -> None:
    assert Messages().get_text() == ""


def test_a_banner_pads_the_text_over_three_lines() -> None:
    banner = Banner(Message("hi"))

    assert banner.get_text() == "\n          \n    hi    \n          \n"


def test_a_banner_formats_each_line() -> None:
    banner = Banner(Message("hi", Formatter(TextColorFormat(TextColor.RED))))

    assert "\033[31m" in banner.get_formatted_text()
