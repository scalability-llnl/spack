# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import spack.util.pattern as pattern


@pytest.fixture()
def interface():
    """Returns the interface class for the composite."""

    class Base:
        counter = 0

        def add(self):
            raise NotImplementedError("add not implemented")

        def subtract(self):
            raise NotImplementedError("subtract not implemented")

    return Base


@pytest.fixture()
def implementation(interface):
    """Returns an implementation of the interface"""

    class Implementation(interface):
        def __init__(self, value):
            self.value = value

        def add(self):
            interface.counter += self.value

        def subtract(self):
            interface.counter -= self.value

    return Implementation


@pytest.fixture(params=["interface", "method_list"])
def composite(interface, implementation, request):
    """Returns a composite that contains an instance of `implementation(1)`
    and one of `implementation(2)`.
    """
    if request.param == "interface":

        @pattern.composite(interface=interface)
        class Composite:
            pass

    else:

        @pattern.composite(method_list=["add", "subtract"])
        class Composite:
            pass

    c = Composite()
    c.append(implementation(1))
    c.append(implementation(2))

    return c


def test_composite_interface_calls(interface, composite):
    composite.add()
    assert interface.counter == 3

    composite.pop()
    composite.subtract()
    assert interface.counter == 2


def test_composite_wrong_container(interface):
    with pytest.raises(TypeError):

        @pattern.composite(interface=interface, container=2)
        class CompositeFromInterface:
            pass


def test_composite_no_methods():
    with pytest.raises(TypeError):

        @pattern.composite()
        class CompositeFromInterface:
            pass
