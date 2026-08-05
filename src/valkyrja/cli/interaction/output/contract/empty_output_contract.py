#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.output.contract.output_contract import OutputContract


class EmptyOutputContract(OutputContract):
    """The contract for an output that writes nothing at all."""
