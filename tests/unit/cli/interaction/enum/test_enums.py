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


def test_exit_code_success_is_zero() -> None:
    assert ExitCode.SUCCESS.value == 0


def test_exit_code_follows_the_sysexits_convention() -> None:
    assert ExitCode.USAGE_ERROR.value == 64
    assert ExitCode.CONFIG_ERROR.value == 78
    assert ExitCode.AUTO_EXIT.value == 255


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
