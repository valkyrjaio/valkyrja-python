#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import re
import sys
from typing import override

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.output.contract.plain_output_contract import PlainOutputContract
from valkyrja.cli.interaction.output.output import Output

TAG_PATTERN = re.compile(r"<[^>]*>")
"""Matches a tag, which PHP removes with `strip_tags`."""


class PlainOutput(Output, PlainOutputContract):
    """An output that writes the plain text, with no tag and no format."""

    @override
    def _output_message(self, message: MessageContract) -> None:
        sys.stdout.write(TAG_PATTERN.sub("", message.get_text()))
