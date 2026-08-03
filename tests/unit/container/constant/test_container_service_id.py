#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for ContainerServiceId.

Each key is part of the public API, so each test pins the whole string. The
TypeScript port holds the same keys.
"""

from valkyrja.container.constant.container_service_id import ContainerServiceId


def test_contract() -> None:
    assert ContainerServiceId.CONTRACT == "Valkyrja.Container.Manager.ContainerContract"


def test_data() -> None:
    assert ContainerServiceId.DATA == "Valkyrja.Container.Data.ContainerData"
