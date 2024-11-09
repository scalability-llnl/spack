# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.builder
import spack.package_base
from spack.directives import build_system, depends_on

from ._checks import BaseBuilder, execute_build_time_tests


class SConsPackage(spack.package_base.PackageBase):
    """Specialized class for packages built using SCons.

    See http://scons.org/documentation.html for more information.
    """

    #: To be used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = "SConsPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "scons"

    build_system("scons")

    depends_on("scons", type="build", when="build_system=scons")


@spack.builder.builder("scons")
class SConsBuilder(BaseBuilder):
    """The Scons builder provides the following phases that can be overridden:

    1. :py:meth:`~.SConsBuilder.build`
    2. :py:meth:`~.SConsBuilder.install`

    Packages that use SCons as a build system are less uniform than packages that use
    other build systems. Developers can add custom subcommands or variables that
    control the build. You will likely need to override
    :py:meth:`~.SConsBuilder.build_args` to pass the appropriate variables.
    """

    #: Phases of a SCons package
    phases = ("build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("build_test",)

    #: Same as legacy_methods, but the signature is different
    legacy_long_methods = ("build_args", "install_args")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ("build_time_test_callbacks",)

    #: Callback names for build-time test
    build_time_test_callbacks = ["build_test"]

    def build_args(self, spec, prefix):
        """Arguments to pass to build."""
        return []

    def build(self, pkg, spec, prefix):
        """Build the package."""
        pkg.module.scons(*self.build_args(spec, prefix))

    def install_args(self, spec, prefix):
        """Arguments to pass to install."""
        return []

    def install(self, pkg, spec, prefix):
        """Install the package."""
        pkg.module.scons("install", *self.install_args(spec, prefix))

    def build_test(self):
        """Run unit tests after build.

        By default, does nothing. Override this if you want to
        add package-specific tests.
        """
        pass

    spack.builder.run_after("build")(execute_build_time_tests)
