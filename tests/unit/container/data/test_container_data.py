#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for ContainerData."""

import dataclasses
from typing import Any

import pytest

from valkyrja.container.data.container_data import ContainerData
from valkyrja.container.manager.contract.container_contract import ContainerContract

SERVICE_ID = "tests.unit.container.Service"


def make_service(container: ContainerContract, arguments: dict[str, Any]) -> object:
    return object()


def publish(container: ContainerContract) -> None:
    return None


def test_the_defaults_are_empty() -> None:
    data = ContainerData()

    assert data.aliases == {}
    assert data.callbacks == {}
    assert data.services == {}
    assert data.singletons == {}


def test_each_default_is_its_own_dictionary() -> None:
    ContainerData().aliases["key"] = "value"

    assert ContainerData().aliases == {}


def test_the_data_holds_what_the_caller_gives() -> None:
    data = ContainerData(
        aliases={"alias": SERVICE_ID},
        callbacks={SERVICE_ID: publish},
        services={SERVICE_ID: make_service},
        singletons={SERVICE_ID: SERVICE_ID},
    )

    assert data.aliases == {"alias": SERVICE_ID}
    assert data.callbacks == {SERVICE_ID: publish}
    assert data.services == {SERVICE_ID: make_service}
    assert data.singletons == {SERVICE_ID: SERVICE_ID}


def test_the_data_is_frozen() -> None:
    data = ContainerData()

    with pytest.raises(dataclasses.FrozenInstanceError):
        data.aliases = {}  # type: ignore[misc]
