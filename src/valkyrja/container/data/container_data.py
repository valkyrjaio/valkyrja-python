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

type PublishCallback = Callable[["ContainerContract"], None]
"""A provider gives this callback for a service, and the container calls it once.

The name of the container is a string. Only the type checker imports that name, so
a reader that evaluates this alias would otherwise raise a `NameError`.
"""

type ServiceFactory = Callable[["ContainerContract", dict[str, Any]], object]
"""The container calls this factory each time it builds a service."""


@dataclass(frozen=True)
class ContainerData:
    aliases: dict[str, str] = field(default_factory=dict)
    callbacks: dict[str, PublishCallback] = field(default_factory=dict)
    services: dict[str, ServiceFactory] = field(default_factory=dict)
    singletons: dict[str, str] = field(default_factory=dict)
