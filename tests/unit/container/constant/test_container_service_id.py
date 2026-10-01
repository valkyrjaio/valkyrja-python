#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for ContainerServiceId.

Each key is part of the public API, so each test pins the whole string. The key
is the import path that Python has, never the path of another port.
"""

from valkyrja.container.constant.container_service_id import ContainerServiceId


def test_contract() -> None:
    assert ContainerServiceId.CONTRACT == "valkyrja.container.manager.ContainerContract"


def test_data() -> None:
    assert ContainerServiceId.DATA == "valkyrja.container.data.ContainerData"
