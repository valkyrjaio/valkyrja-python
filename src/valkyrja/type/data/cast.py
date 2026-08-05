#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from dataclasses import dataclass

from valkyrja.type.enum.cast_type import CastType


@dataclass(frozen=True)
class Cast:
    """Says what type a value becomes, and how the framework converts it."""

    type: str
    convert: bool = True
    is_array: bool = False

    @staticmethod
    def from_cast_type(cast_type: CastType, convert: bool = True, is_array: bool = False) -> Cast:
        """Build a cast from a member of `CastType`."""
        return Cast(type=cast_type.value, convert=convert, is_array=is_array)
