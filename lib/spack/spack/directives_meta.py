# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections.abc
import functools
from typing import List, Set

import llnl.util.lang

import spack.error
import spack.spec

#: Names of possible directives. This list is mostly populated using the @directive decorator.
#: Some directives leverage others and in that case are not automatically added.
directive_names = ["build_system"]


class DirectiveMeta(type):
    """Flushes the directives that were temporarily stored in the staging
    area into the package.
    """

    # Set of all known directives
    _directive_dict_names: Set[str] = set()
    _directives_to_be_executed: List[str] = []
    _when_constraints_from_context: List[str] = []
    _default_args: List[dict] = []

    def __new__(cls, name, bases, attr_dict):
        # Initialize the attribute containing the list of directives
        # to be executed. Here we go reversed because we want to execute
        # commands:
        # 1. in the order they were defined
        # 2. following the MRO
        attr_dict["_directives_to_be_executed"] = []
        for base in reversed(bases):
            try:
                directive_from_base = base._directives_to_be_executed
                attr_dict["_directives_to_be_executed"].extend(directive_from_base)
            except AttributeError:
                # The base class didn't have the required attribute.
                # Continue searching
                pass

        # De-duplicates directives from base classes
        attr_dict["_directives_to_be_executed"] = [
            x for x in llnl.util.lang.dedupe(attr_dict["_directives_to_be_executed"])
        ]

        # Move things to be executed from module scope (where they
        # are collected first) to class scope
        if DirectiveMeta._directives_to_be_executed:
            attr_dict["_directives_to_be_executed"].extend(
                DirectiveMeta._directives_to_be_executed
            )
            DirectiveMeta._directives_to_be_executed = []

        return super(DirectiveMeta, cls).__new__(cls, name, bases, attr_dict)

    def __init__(cls, name, bases, attr_dict):
        # The instance is being initialized: if it is a package we must ensure
        # that the directives are called to set it up.

        if "spack.pkg" in cls.__module__:
            # Ensure the presence of the dictionaries associated with the directives.
            # All dictionaries are defaultdicts that create lists for missing keys.
            for d in DirectiveMeta._directive_dict_names:
                setattr(cls, d, {})

            # Lazily execute directives
            for directive in cls._directives_to_be_executed:
                directive(cls)

            # Ignore any directives executed *within* top-level
            # directives by clearing out the queue they're appended to
            DirectiveMeta._directives_to_be_executed = []

        super(DirectiveMeta, cls).__init__(name, bases, attr_dict)

    @staticmethod
    def push_to_context(when_spec):
        """Add a spec to the context constraints."""
        DirectiveMeta._when_constraints_from_context.append(when_spec)

    @staticmethod
    def pop_from_context():
        """Pop the last constraint from the context"""
        return DirectiveMeta._when_constraints_from_context.pop()

    @staticmethod
    def push_default_args(default_args):
        """Push default arguments"""
        DirectiveMeta._default_args.append(default_args)

    @staticmethod
    def pop_default_args():
        """Pop default arguments"""
        return DirectiveMeta._default_args.pop()

    @staticmethod
    def directive(dicts=None):
        """Decorator for Spack directives.

        Spack directives allow you to modify a package while it is being
        defined, e.g. to add version or dependency information.  Directives
        are one of the key pieces of Spack's package "language", which is
        embedded in python.

        Here's an example directive:

        .. code-block:: python

            @directive(dicts='versions')
            version(pkg, ...):
                ...

        This directive allows you write:

        .. code-block:: python

            class Foo(Package):
                version(...)

        The ``@directive`` decorator handles a couple things for you:

          1. Adds the class scope (pkg) as an initial parameter when
             called, like a class method would.  This allows you to modify
             a package from within a directive, while the package is still
             being defined.

          2. It automatically adds a dictionary called "versions" to the
             package so that you can refer to pkg.versions.

        The ``(dicts='versions')`` part ensures that ALL packages in Spack
        will have a ``versions`` attribute after they're constructed, and
        that if no directive actually modified it, it will just be an
        empty dict.

        This is just a modular way to add storage attributes to the
        Package class, and it's how Spack gets information from the
        packages to the core.
        """
        global directive_names

        if isinstance(dicts, str):
            dicts = (dicts,)

        if not isinstance(dicts, collections.abc.Sequence):
            message = "dicts arg must be list, tuple, or string. Found {0}"
            raise TypeError(message.format(type(dicts)))

        # Add the dictionary names if not already there
        DirectiveMeta._directive_dict_names |= set(dicts)

        # This decorator just returns the directive functions
        def _decorator(decorated_function):
            directive_names.append(decorated_function.__name__)

            @functools.wraps(decorated_function)
            def _wrapper(*args, **_kwargs):
                # First merge default args with kwargs
                kwargs = dict()
                for default_args in DirectiveMeta._default_args:
                    kwargs.update(default_args)
                kwargs.update(_kwargs)

                # Inject when arguments from the context
                if DirectiveMeta._when_constraints_from_context:
                    # Check that directives not yet supporting the when= argument
                    # are not used inside the context manager
                    if decorated_function.__name__ == "version":
                        msg = (
                            'directive "{0}" cannot be used within a "when"'
                            ' context since it does not support a "when=" '
                            "argument"
                        )
                        msg = msg.format(decorated_function.__name__)
                        raise DirectiveError(msg)

                    when_constraints = [
                        spack.spec.Spec(x) for x in DirectiveMeta._when_constraints_from_context
                    ]
                    if kwargs.get("when"):
                        when_constraints.append(spack.spec.Spec(kwargs["when"]))
                    when_spec = spack.spec.merge_abstract_anonymous_specs(*when_constraints)

                    kwargs["when"] = when_spec

                # If any of the arguments are executors returned by a
                # directive passed as an argument, don't execute them
                # lazily. Instead, let the called directive handle them.
                # This allows nested directive calls in packages.  The
                # caller can return the directive if it should be queued.
                def remove_directives(arg):
                    directives = DirectiveMeta._directives_to_be_executed
                    if isinstance(arg, (list, tuple)):
                        # Descend into args that are lists or tuples
                        for a in arg:
                            remove_directives(a)
                    else:
                        # Remove directives args from the exec queue
                        remove = next((d for d in directives if d is arg), None)
                        if remove is not None:
                            directives.remove(remove)

                # Nasty, but it's the best way I can think of to avoid
                # side effects if directive results are passed as args
                remove_directives(args)
                remove_directives(list(kwargs.values()))

                # A directive returns either something that is callable on a
                # package or a sequence of them
                result = decorated_function(*args, **kwargs)

                # ...so if it is not a sequence make it so
                values = result
                if not isinstance(values, collections.abc.Sequence):
                    values = (values,)

                DirectiveMeta._directives_to_be_executed.extend(values)

                # wrapped function returns same result as original so
                # that we can nest directives
                return result

            return _wrapper

        return _decorator


class DirectiveError(spack.error.SpackError):
    """This is raised when something is wrong with a package directive."""
