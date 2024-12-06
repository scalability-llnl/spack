# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains utilities for using multi-methods in
spack. You can think of multi-methods like overloaded methods --
they're methods with the same name, and we need to select a version
of the method based on some criteria.  e.g., for overloaded
methods, you would select a version of the method to call based on
the types of its arguments.

In spack, multi-methods are used to ease the life of package
authors.  They allow methods like install() (or other methods
called by install()) to declare multiple versions to be called when
the package is instantiated with different specs.  e.g., if the
package is built with OpenMPI on x86_64,, you might want to call a
different install method than if it was built for mpich2 on
BlueGene/Q.  Likewise, you might want to do a different type of
install for different versions of the package.

Multi-methods provide a simple decorator-based syntax for this that
avoids overly complicated rat nests of if statements.  Obviously,
depending on the scenario, regular old conditionals might be clearer,
so package authors should use their judgement.
"""
import functools
from contextlib import contextmanager

import spack.directives_meta
import spack.error
import spack.spec


class MultiMethodMeta(type):
    """This allows us to track the class's dict during instantiation."""

    #: saved dictionary of attrs on the class being constructed
    _locals = None

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        """Save the dictionary that will be used for the class namespace."""
        MultiMethodMeta._locals = dict()
        return MultiMethodMeta._locals

    def __init__(cls, name, bases, attr_dict):
        """Clear out the cached locals dict once the class is built."""
        MultiMethodMeta._locals = None
        super(MultiMethodMeta, cls).__init__(name, bases, attr_dict)


class SpecMultiMethod:
    """This implements a multi-method for Spack specs.  Packages are
    instantiated with a particular spec, and you may want to
    execute different versions of methods based on what the spec
    looks like.  For example, you might want to call a different
    version of install() for one platform than you call on another.

    The SpecMultiMethod class implements a callable object that
    handles method dispatch.  When it is called, it looks through
    registered methods and their associated specs, and it tries
    to find one that matches the package's spec.  If it finds one
    (and only one), it will call that method.

    This is intended for use with decorators (see below).  The
    decorator (see docs below) creates SpecMultiMethods and
    registers method versions with them.

    To register a method, you can do something like this:
        mm = SpecMultiMethod()
        mm.register("^chaos_5_x86_64_ib", some_method)

    The object registered needs to be a Spec or some string that
    will parse to be a valid spec.

    When the mm is actually called, it selects a version of the
    method to call based on the sys_type of the object it is
    called on.

    See the docs for decorators below for more details.
    """

    def __init__(self, default=None):
        self.method_list = []
        self.default = default
        if default:
            functools.update_wrapper(self, default)

    def register(self, spec, method):
        """Register a version of a method for a particular spec."""
        self.method_list.append((spec, method))

        if not hasattr(self, "__name__"):
            functools.update_wrapper(self, method)
        else:
            assert self.__name__ == method.__name__

    def __get__(self, obj, objtype):
        """This makes __call__ support instance methods."""
        # Method_list is a list of tuples (constraint, method)
        # Here we are going to assume that we have at least one
        # element in the list. The first registered function
        # will be the one 'wrapped'.
        wrapped_method = self.method_list[0][1]

        # Call functools.wraps manually to get all the attributes
        # we need to be disguised as the wrapped_method
        func = functools.wraps(wrapped_method)(functools.partial(self.__call__, obj))
        return func

    def _get_method_by_spec(self, spec):
        """Find the method of this SpecMultiMethod object that satisfies the
        given spec, if one exists
        """
        for condition, method in self.method_list:
            if spec.satisfies(condition):
                return method
        return self.default or None

    def __call__(self, package_or_builder_self, *args, **kwargs):
        """Find the first method with a spec that matches the
        package's spec.  If none is found, call the default
        or if there is none, then raise a NoSuchMethodError.
        """
        spec_method = self._get_method_by_spec(package_or_builder_self.spec)
        if spec_method:
            return spec_method(package_or_builder_self, *args, **kwargs)
        # Unwrap the MRO of `package_self by hand. Note that we can't
        # use `super()` here, because using `super()` recursively
        # requires us to know the class of `package_self`, as well as
        # its superclasses for successive calls. We don't have that
        # information within `SpecMultiMethod`, because it is not
        # associated with the package class.
        for cls in package_or_builder_self.__class__.__mro__[1:]:
            superself = cls.__dict__.get(self.__name__, None)

            if isinstance(superself, SpecMultiMethod):
                # Check parent multimethod for method for spec.
                superself_method = superself._get_method_by_spec(package_or_builder_self.spec)
                if superself_method:
                    return superself_method(package_or_builder_self, *args, **kwargs)
            elif superself:
                return superself(package_or_builder_self, *args, **kwargs)

        raise NoSuchMethodError(
            type(package_or_builder_self),
            self.__name__,
            package_or_builder_self.spec,
            [m[0] for m in self.method_list],
        )


class when:
    def __init__(self, condition):
        """Can be used both as a decorator, for multimethods, or as a context
        manager to group ``when=`` arguments together.

        Examples are given in the docstrings below.

        Args:
            condition (str): condition to be met
        """
        if isinstance(condition, bool):
            self.spec = spack.spec.Spec() if condition else None
        else:
            self.spec = spack.spec.Spec(condition)

    def __call__(self, method):
        """This annotation lets packages declare multiple versions of
        methods like install() that depend on the package's spec.

        For example:

           .. code-block:: python

              class SomePackage(Package):
                  ...

                  def install(self, prefix):
                      # Do default install

                  @when('target=x86_64:')
                  def install(self, prefix):
                      # This will be executed instead of the default install if
                      # the package's target is in the x86_64 family.

                  @when('target=ppc64:')
                  def install(self, prefix):
                      # This will be executed if the package's target is in
                      # the ppc64 family

           This allows each package to have a default version of install() AND
           specialized versions for particular platforms.  The version that is
           called depends on the architecutre of the instantiated package.

           Note that this works for methods other than install, as well.  So,
           if you only have part of the install that is platform specific, you
           could do this:

           .. code-block:: python

              class SomePackage(Package):
                  ...
                  # virtual dependence on MPI.
                  # could resolve to mpich, mpich2, OpenMPI
                  depends_on('mpi')

                  def setup(self):
                      # do nothing in the default case
                      pass

                  @when('^openmpi')
                  def setup(self):
                      # do something special when this is built with OpenMPI for
                      # its MPI implementations.


                  def install(self, prefix):
                      # Do common install stuff
                      self.setup()
                      # Do more common install stuff

           Note that the default version of decorated methods must
           *always* come first.  Otherwise it will override all of the
           platform-specific versions.  There's not much we can do to get
           around this because of the way decorators work.
        """
        assert (
            MultiMethodMeta._locals is not None
        ), "cannot use multimethod, missing MultiMethodMeta metaclass?"

        # Create a multimethod with this name if there is not one already
        original_method = MultiMethodMeta._locals.get(method.__name__)
        if not isinstance(original_method, SpecMultiMethod):
            original_method = SpecMultiMethod(original_method)

        if self.spec is not None:
            original_method.register(self.spec, method)

        return original_method

    def __enter__(self):
        """Inject the constraint spec into the `when=` argument of directives
        in the context.

        This context manager allows you to write:

            with when('+nvptx'):
                conflicts('@:6', msg='NVPTX only supported from gcc 7')
                conflicts('languages=ada')
                conflicts('languages=brig')

        instead of writing:

             conflicts('@:6', when='+nvptx', msg='NVPTX only supported from gcc 7')
             conflicts('languages=ada', when='+nvptx')
             conflicts('languages=brig', when='+nvptx')

        Context managers can be nested (but this is not recommended for readability)
        and add their constraint to whatever may be already present in the directive
        `when=` argument.
        """
        spack.directives_meta.DirectiveMeta.push_to_context(str(self.spec))

    def __exit__(self, exc_type, exc_val, exc_tb):
        spack.directives_meta.DirectiveMeta.pop_from_context()


@contextmanager
def default_args(**kwargs):
    spack.directives_meta.DirectiveMeta.push_default_args(kwargs)
    yield
    spack.directives_meta.DirectiveMeta.pop_default_args()


class MultiMethodError(spack.error.SpackError):
    """Superclass for multimethod dispatch errors"""

    def __init__(self, message):
        super().__init__(message)


class NoSuchMethodError(spack.error.SpackError):
    """Raised when we can't find a version of a multi-method."""

    def __init__(self, cls, method_name, spec, possible_specs):
        super().__init__(
            "Package %s does not support %s called with %s.  Options are: %s"
            % (cls.__name__, method_name, spec, ", ".join(str(s) for s in possible_specs))
        )
