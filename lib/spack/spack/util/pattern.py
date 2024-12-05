# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections.abc
import functools
import inspect


class Delegate:
    def __init__(self, name, container):
        self.name = name
        self.container = container

    def __call__(self, *args, **kwargs):
        return [getattr(item, self.name)(*args, **kwargs) for item in self.container]


class Composite(list):
    def __init__(self, fns_to_delegate):
        self.fns_to_delegate = fns_to_delegate

    def __getattr__(self, name):
        if name != "fns_to_delegate" and name in self.fns_to_delegate:
            return Delegate(name, self)
        else:
            return self.__getattribute__(name)


def composite(interface=None, method_list=None, container=list):
    """Decorator implementing the GoF composite pattern.

    Args:
        interface (type): class exposing the interface to which the
            composite object must conform. Only non-private and
            non-special methods will be taken into account
        method_list (list): names of methods that should be part
            of the composite
        container (collections.abc.MutableSequence): container for the composite object
            (default = list).  Must fulfill the MutableSequence
            contract. The composite class will expose the container API
            to manage object composition

    Returns:
        a class decorator that patches a class adding all the methods
        it needs to be a composite for a given interface.

    """
    # Check if container fulfills the MutableSequence contract and raise an
    # exception if it doesn't. The patched class returned by the decorator will
    # inherit from the container class to expose the interface needed to manage
    # objects composition
    if not issubclass(container, collections.abc.MutableSequence):
        raise TypeError("Container must fulfill the MutableSequence contract")

    # Check if at least one of the 'interface' or the 'method_list' arguments
    # are defined
    if interface is None and method_list is None:
        raise TypeError(
            "Either 'interface' or 'method_list' must be defined on a call " "to composite"
        )

    def cls_decorator(cls):
        # Retrieve the base class of the composite. Inspect its methods and
        # decide which ones will be overridden
        def no_special_no_private(x):
            return callable(x) and not x.__name__.startswith("_")

        # Patch the behavior of each of the methods in the previous list.
        # This is done associating an instance of the descriptor below to
        # any method that needs to be patched.
        class IterateOver:
            """Decorator used to patch methods in a composite.

            It iterates over all the items in the instance containing the
            associated attribute and calls for each of them an attribute
            with the same name
            """

            def __init__(self, name, func=None):
                self.name = name
                self.func = func

            def __get__(self, instance, owner):
                def getter(*args, **kwargs):
                    for item in instance:
                        getattr(item, self.name)(*args, **kwargs)

                # If we are using this descriptor to wrap a method from an
                # interface, then we must conditionally use the
                # `functools.wraps` decorator to set the appropriate fields
                if self.func is not None:
                    getter = functools.wraps(self.func)(getter)
                return getter

        dictionary_for_type_call = {}

        # Construct a dictionary with the methods explicitly passed as name
        if method_list is not None:
            dictionary_for_type_call.update((name, IterateOver(name)) for name in method_list)

        # Construct a dictionary with the methods inspected from the interface
        if interface is not None:
            dictionary_for_type_call.update(
                (name, IterateOver(name, method))
                for name, method in inspect.getmembers(interface, predicate=no_special_no_private)
            )

        # Get the methods that are defined in the scope of the composite
        # class and override any previous definition
        dictionary_for_type_call.update(
            (name, method) for name, method in inspect.getmembers(cls, predicate=inspect.ismethod)
        )

        # Generate the new class on the fly and return it
        # FIXME : inherit from interface if we start to use ABC classes?
        wrapper_class = type(cls.__name__, (cls, container), dictionary_for_type_call)
        return wrapper_class

    return cls_decorator


class Bunch:
    """Carries a bunch of named attributes (from Alex Martelli bunch)"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Args(Bunch):
    """Subclass of Bunch to write argparse args more naturally."""

    def __init__(self, *flags, **kwargs):
        super().__init__(flags=tuple(flags), kwargs=kwargs)
