#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final


@final
class ClassNameFactory:
    """Builds the string that names a class.

    Every port needs one name for a class, because a binding key, an event id,
    and a cache entry all hold that name as a string. PHP writes `Foo::class`
    and Java writes `Foo.class`. Python has no such operator, so this factory
    builds the name.
    """

    @staticmethod
    def class_(cls: type) -> str:
        """Get the name of a class, with the module in front of it.

        The name ends in an underscore, because `class` is a reserved word.
        """
        return f"{cls.__module__}.{cls.__qualname__}"

    @staticmethod
    def class_of(instance: object) -> str:
        """Get the name of the class of an object."""
        return ClassNameFactory.class_(type(instance))
