#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from valkyrja.container.manager.contract.container_contract import ContainerContract

type PublishCallback = Callable[[ContainerContract], None]
"""A provider gives this callback for a service, and the container calls it once."""

type ServiceFactory = Callable[[ContainerContract, dict[str, Any]], object]
"""The container calls this factory each time it builds a service."""


@dataclass(frozen=True)
class ContainerData:
    """A data representation of the state of a container.

    `sindri` writes this same shape into the generated cache, so the container
    loads a cache the way it loads its own state.
    """

    aliases: dict[str, str] = field(default_factory=dict)
    callbacks: dict[str, PublishCallback] = field(default_factory=dict)
    services: dict[str, ServiceFactory] = field(default_factory=dict)
    singletons: dict[str, str] = field(default_factory=dict)
