# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.platforms
from spack.package import *
from spack.pkg.builtin.mock.multimethod_base import MultimethodBase


class Multimethod(MultimethodBase):
    """This package is designed for use with Spack's multimethod test.
    It has a bunch of test cases for the @when decorator that the
    test uses.
    """

    homepage = "http://www.example.com/"
    url = "http://www.example.com/example-1.0.tar.gz"

    version("5.0", md5="0123456789abcdef0123456789abcdef")
    version("4.0", md5="0123456789abcdef0123456789abcdef")
    version("3.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="0123456789abcdef0123456789abcdef")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("mpi", default=False, description="")

    depends_on("mpi", when="+mpi")

    #
    # These functions are only valid for versions 1, 3, and 4.
    #
    @when("@1.0")
    def no_version_2(self):
        return 1

    @when("@3.0")
    def no_version_2(self):
        return 3

    @when("@4.0")
    def no_version_2(self):
        return 4

    #
    # These functions overlap, so there is ambiguity, but we'll take
    # the first one.
    #
    @when("@:4")
    def version_overlap(self):
        return 1

    @when("@2:")
    def version_overlap(self):
        return 2

    #
    # More complicated case with cascading versions.
    #
    def mpi_version(self):
        return 0

    @when("^mpi@3:")
    def mpi_version(self):
        return 3

    @when("^mpi@2:")
    def mpi_version(self):
        return 2

    @when("^mpi@1:")
    def mpi_version(self):
        return 1

    #
    # Use these to test whether the default method is called when no
    # match is found.  This also tests whether we can switch methods
    # on compilers
    #
    def has_a_default(self):
        return "default"

    @when("%gcc")
    def has_a_default(self):
        return "gcc"

    @when("%clang")
    def has_a_default(self):
        return "clang"

    #
    # Make sure we can switch methods on different target
    #
    platform = spack.platforms.host()
    targets = list(platform.targets.values())
    if len(targets) > 1:
        targets = targets[:-1]

    for target in targets:

        @when("target=" + target.name)
        def different_by_target(self):
            if isinstance(self.spec.architecture.target, str):
                return self.spec.architecture.target
            else:
                return self.spec.architecture.target.name

    #
    # Make sure we can switch methods on different dependencies
    #

    @when("^mpich")
    def different_by_dep(self):
        return "mpich"

    @when("^zmpi")
    def different_by_dep(self):
        return "zmpi"

    #
    # Make sure we can switch on virtual dependencies
    #
    def different_by_virtual_dep(self):
        return 1

    @when("^mpi@2:")
    def different_by_virtual_dep(self):
        return 2

    #
    # Make sure methods with a default implementation in a superclass
    # will invoke that method when none in the subclass match.
    #
    @when("@2:")
    def base_method(self):
        return "multimethod"

    #
    # Make sure methods with non-default implementations in a superclass
    # will invoke those methods when none in the subclass match but one in
    # the superclass does.
    #
    @when("@1.0")
    def inherited_and_overridden(self):
        return "base@1.0"

    @when("@2.0")
    def inherited_and_overridden(self):
        return "base@2.0"

    #
    # Make sure that multimethods follow MRO properly with diamond inheritance
    #
    @when("@2.0")
    def diamond_inheritance(self):
        return "first_parent"

    @when("@4.0")
    def diamond_inheritance(self):
        return "should_not_be_reached by diamond inheritance test"

    #
    # Check that multimethods work with boolean values
    #
    @when(True)
    def boolean_true_first(self):
        return "True"

    @when(False)
    def boolean_true_first(self):
        return "False"

    @when(False)
    def boolean_false_first(self):
        return "False"

    @when(True)
    def boolean_false_first(self):
        return "True"
