#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for ClassNameFactory."""

from valkyrja.event.data.listener import Listener
from valkyrja.support.factory.class_name_factory import ClassNameFactory


class Outer:
    class Inner:
        pass


def test_class_names_the_module_and_the_class() -> None:
    assert ClassNameFactory.class_(Listener) == "valkyrja.event.data.listener.Listener"


def test_class_keeps_the_outer_class_of_a_nested_class() -> None:
    assert ClassNameFactory.class_(Outer.Inner).endswith("Outer.Inner")


def test_class_of_reads_the_class_of_an_object() -> None:
    listener = Listener("event", "name", lambda container, arguments: None)

    assert ClassNameFactory.class_of(listener) == ClassNameFactory.class_(Listener)
