#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for InvalidReferenceMode."""

from valkyrja.container.enum.invalid_reference_mode import InvalidReferenceMode


def test_the_enum_has_both_modes() -> None:
    assert list(InvalidReferenceMode) == [
        InvalidReferenceMode.NEW_INSTANCE_OR_THROW_EXCEPTION,
        InvalidReferenceMode.THROW_EXCEPTION,
    ]


def test_each_mode_carries_its_own_value() -> None:
    assert len({mode.value for mode in InvalidReferenceMode}) == len(InvalidReferenceMode)
