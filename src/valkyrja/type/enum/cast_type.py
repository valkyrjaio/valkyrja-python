#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum


class CastType(Enum):
    """The type that a cast converts a value to.

    Warning: each member holds a STRING that names the type, never the class
    itself. PHP writes `StringT::class`, and Java writes `StringT.class`. Python
    that named the 12 classes would import every one of them to read any one of
    them, which is the eager-import cost that a string binding key exists to
    avoid. The container resolves the string when a cast runs.
    """

    STRING = "valkyrja.type.string.StringT"
    INT = "valkyrja.type.int.IntT"
    FLOAT = "valkyrja.type.float.FloatT"
    BOOL = "valkyrja.type.bool.BoolT"
    ARRAY = "valkyrja.type.array.ArrayT"
    OBJECT = "valkyrja.type.object.ObjectT"
    SERIALIZED_OBJECT = "valkyrja.type.object.SerializedObject"
    JSON = "valkyrja.type.json.Json"
    JSON_OBJECT = "valkyrja.type.json.JsonObject"
    TRUE = "valkyrja.type.bool.TrueT"
    FALSE = "valkyrja.type.bool.FalseT"
    NULL = "valkyrja.type.null.NullT"
