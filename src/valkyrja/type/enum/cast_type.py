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

    STRING = "Valkyrja.Type.String.StringT"
    INT = "Valkyrja.Type.Int.IntT"
    FLOAT = "Valkyrja.Type.Float.FloatT"
    BOOL = "Valkyrja.Type.Bool.BoolT"
    ARRAY = "Valkyrja.Type.Array.ArrayT"
    OBJECT = "Valkyrja.Type.Object.ObjectT"
    SERIALIZED_OBJECT = "Valkyrja.Type.Object.SerializedObject"
    JSON = "Valkyrja.Type.Json.Json"
    JSON_OBJECT = "Valkyrja.Type.Json.JsonObject"
    TRUE = "Valkyrja.Type.Bool.TrueT"
    FALSE = "Valkyrja.Type.Bool.FalseT"
    NULL = "Valkyrja.Type.Null.NullT"
