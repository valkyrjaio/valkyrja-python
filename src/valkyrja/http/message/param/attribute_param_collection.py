#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.http.message.param.contract.attribute_param_collection_contract import AttributeParamCollectionContract
from valkyrja.http.message.param.param_collection import ParamCollection


@final
class AttributeParamCollection(ParamCollection, AttributeParamCollectionContract):
    """The parameters that attribute carries."""
