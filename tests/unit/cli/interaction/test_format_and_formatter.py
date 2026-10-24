#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the formats and the formatters."""

import pytest

from valkyrja.cli.interaction.enum.background_color import DEFAULT_BACKGROUND_COLOR, BackgroundColor
from valkyrja.cli.interaction.enum.style import Style
from valkyrja.cli.interaction.enum.text_color import DEFAULT_TEXT_COLOR, TextColor
from valkyrja.cli.interaction.format.background_color_format import BackgroundColorFormat
from valkyrja.cli.interaction.format.format import Format
from valkyrja.cli.interaction.format.style_format import StyleFormat
from valkyrja.cli.interaction.format.text_color_format import TextColorFormat
from valkyrja.cli.interaction.formatter.error_formatter import ErrorFormatter
from valkyrja.cli.interaction.formatter.formatter import Formatter
from valkyrja.cli.interaction.formatter.highlighted_text_formatter import HighlightedTextFormatter
from valkyrja.cli.interaction.formatter.question_formatter import QuestionFormatter
from valkyrja.cli.interaction.formatter.success_formatter import SuccessFormatter
from valkyrja.cli.interaction.formatter.warning_formatter import WarningFormatter


def test_a_format_holds_both_codes() -> None:
    format_ = Format("1", "22")

    assert format_.get_set_code() == "1"
    assert format_.get_unset_code() == "22"


def test_with_set_code_returns_a_copy() -> None:
    format_ = Format("1", "22")

    changed = format_.with_set_code("4")

    assert changed is not format_
    assert changed.get_set_code() == "4"
    assert format_.get_set_code() == "1"


def test_with_unset_code_returns_a_copy() -> None:
    format_ = Format("1", "22")

    changed = format_.with_unset_code("24")

    assert changed is not format_
    assert changed.get_unset_code() == "24"
    assert format_.get_unset_code() == "22"


def test_a_text_color_format_reads_the_enum() -> None:
    format_ = TextColorFormat(TextColor.RED)

    assert format_.get_set_code() == str(TextColor.RED.value)
    assert format_.get_unset_code() == str(DEFAULT_TEXT_COLOR)


def test_a_background_color_format_reads_the_enum() -> None:
    format_ = BackgroundColorFormat(BackgroundColor.GREEN)

    assert format_.get_set_code() == str(BackgroundColor.GREEN.value)
    assert format_.get_unset_code() == str(DEFAULT_BACKGROUND_COLOR)


def test_a_style_format_reads_the_enum() -> None:
    format_ = StyleFormat(Style.BOLD)

    assert format_.get_set_code() == "1"
    assert format_.get_unset_code() == "22"


def test_a_formatter_with_no_format_returns_the_text() -> None:
    assert Formatter().format_text("plain") == "plain"


def test_a_formatter_puts_each_code_around_the_text() -> None:
    formatter = Formatter(TextColorFormat(TextColor.RED))

    assert formatter.format_text("red") == "\033[31mred\033[39m"


def test_a_formatter_joins_several_codes() -> None:
    formatter = Formatter(TextColorFormat(TextColor.RED), StyleFormat(Style.BOLD))

    assert formatter.format_text("x") == "\033[31;1mx\033[39;22m"


def test_get_formats_copies_the_list() -> None:
    formatter = Formatter(TextColorFormat(TextColor.RED))

    formatter.get_formats().clear()

    assert len(formatter.get_formats()) == 1


def test_with_formats_returns_a_copy() -> None:
    formatter = Formatter(TextColorFormat(TextColor.RED))

    changed = formatter.with_formats()

    assert changed is not formatter
    assert changed.get_formats() == []
    assert len(formatter.get_formats()) == 1


@pytest.mark.parametrize(
    ("formatter", "count"),
    [
        (ErrorFormatter(), 2),
        (SuccessFormatter(), 2),
        (WarningFormatter(), 2),
        (HighlightedTextFormatter(), 1),
        (QuestionFormatter(), 1),
    ],
)
def test_each_named_formatter_carries_its_formats(formatter: Formatter, count: int) -> None:
    assert len(formatter.get_formats()) == count
    assert formatter.format_text("x") != "x"
