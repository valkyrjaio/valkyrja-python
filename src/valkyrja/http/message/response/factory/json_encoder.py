#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import json
import re
from typing import Any, Final, final

HTML_ESCAPES: Final[dict[str, str]] = {
    "<": "\\u003C",
    ">": "\\u003E",
    "&": "\\u0026",
    "'": "\\u0027",
}
"""Each character that closes a tag or an attribute when a page embeds the json.

PHP writes these with `JSON_HEX_TAG`, `JSON_HEX_AMP`, and `JSON_HEX_APOS`. None of
them carries meaning in json syntax, so each one appears inside a string alone.
"""

ESCAPED_PAIR_PATTERN: Final[re.Pattern[str]] = re.compile(r'\\(["\\])')
"""One backslash and the character it escapes, which is a quote or a backslash."""


@final
class JsonEncoder:
    @staticmethod
    def get_encoded(data: Any) -> str:
        """Get the json that PHP writes for the same data.

        PHP passes the flags that add up to 79, which escape each character a page
        reads as markup and leave a forward slash as it is. A float that is not a
        number reports a failure, rather than reaching the body as a word that no
        reader parses.
        """
        encoded = json.dumps(data, allow_nan=False, separators=(",", ":"))

        for character, escape in HTML_ESCAPES.items():
            encoded = encoded.replace(character, escape)

        return JsonEncoder._get_quotes_escaped(encoded)

    @staticmethod
    def get_decoded(encoded: str) -> Any:
        """Get the data that one json document holds."""
        return json.loads(encoded)

    @staticmethod
    def _get_quotes_escaped(encoded: str) -> str:
        """Get the json with each escaped quote written as a hexadecimal escape.

        PHP writes a quote inside a string with `JSON_HEX_QUOT`. The walk reads one
        backslash pair at a time, so a literal backslash keeps the quote after it.
        """
        return ESCAPED_PAIR_PATTERN.sub(lambda match: "\\u0022" if match.group(1) == '"' else "\\\\", encoded)
