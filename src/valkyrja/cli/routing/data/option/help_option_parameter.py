#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.routing.constant.option_name import OptionName
from valkyrja.cli.routing.constant.option_short_name import OptionShortName
from valkyrja.cli.routing.data.option_parameter import OptionParameter
from valkyrja.cli.routing.enum.option_value_mode import OptionValueMode


class HelpOptionParameter(OptionParameter):
    """The `--help` option that every command accepts."""

    def __init__(self) -> None:
        super().__init__(
            name=OptionName.HELP,
            description="Help with this command",
            short_names=[OptionShortName.HELP],
            value_mode=OptionValueMode.NONE,
        )
