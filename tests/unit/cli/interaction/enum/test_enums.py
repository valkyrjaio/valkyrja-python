#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the enums of the Cli Interaction subcomponent."""

import pytest

from valkyrja.cli.interaction.enum.background_color import (
    DEFAULT_BACKGROUND_COLOR,
    BackgroundColor,
)
from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.enum.option_type import OptionType
from valkyrja.cli.interaction.enum.style import DEFAULT_STYLE, Style
from valkyrja.cli.interaction.enum.text_color import DEFAULT_TEXT_COLOR, TextColor

EXIT_CODES = [
    (ExitCode.SUCCESS, 0),
    (ExitCode.ERROR, 1),
    (ExitCode.USAGE_ERROR, 64),
    (ExitCode.DATA_ERROR, 65),
    (ExitCode.NO_INPUT, 67),
    (ExitCode.NO_USER, 68),
    (ExitCode.UNAVAILABLE, 69),
    (ExitCode.SOFTWARE_ERROR, 70),
    (ExitCode.OS_ERROR, 71),
    (ExitCode.OS_FILE_ERROR, 72),
    (ExitCode.CANT_CREATE, 73),
    (ExitCode.IO_ERROR, 74),
    (ExitCode.TEMP_FAIL, 75),
    (ExitCode.PROTOCOL_ERROR, 76),
    (ExitCode.NO_PERMISSION, 77),
    (ExitCode.CONFIG_ERROR, 78),
    (ExitCode.AUTO_EXIT, 255),
]


@pytest.mark.parametrize(("exit_code", "value"), EXIT_CODES)
def test_every_exit_code_keeps_its_number(exit_code: ExitCode, value: int) -> None:
    assert exit_code.value == value


def test_the_table_covers_every_exit_code() -> None:
    # A member added to the enum and missed above would otherwise go unpinned.
    assert [exit_code for exit_code, _ in EXIT_CODES] == list(ExitCode)


def test_exit_code_is_an_integer() -> None:
    assert isinstance(ExitCode.ERROR, int)


def test_option_type_has_both_forms() -> None:
    assert list(OptionType) == [OptionType.SHORT, OptionType.LONG]


@pytest.mark.parametrize("color", list(TextColor))
def test_every_text_color_returns_the_default(color: TextColor) -> None:
    assert color.get_default() == DEFAULT_TEXT_COLOR


def test_text_color_values() -> None:
    assert TextColor.BLACK.value == 30
    assert TextColor.LIGHT_WHITE.value == 97


@pytest.mark.parametrize("color", list(BackgroundColor))
def test_every_background_color_returns_the_default(color: BackgroundColor) -> None:
    assert color.get_default() == DEFAULT_BACKGROUND_COLOR


def test_background_color_values() -> None:
    assert BackgroundColor.BLACK.value == 40
    assert BackgroundColor.LIGHT_WHITE.value == 107


@pytest.mark.parametrize(
    ("style", "expected"),
    [
        (Style.BOLD, 22),
        (Style.UNDERSCORE, 24),
        (Style.BLINK, 25),
        (Style.INVERSE, 27),
        (Style.CONCEAL, DEFAULT_STYLE),
    ],
)
def test_each_style_ends_with_its_own_code(style: Style, expected: int) -> None:
    assert style.get_default() == expected


def test_every_style_has_a_case_in_get_default() -> None:
    """Each style is covered above, so the default arm is reached by CONCEAL alone."""
    assert {style.get_default() for style in Style} == {22, 24, 25, 27, DEFAULT_STYLE}
