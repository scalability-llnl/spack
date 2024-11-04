# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from typing import Iterable

from llnl.util.filesystem import filter_file, find
from llnl.util.lang import memoized

import spack.builder
import spack.package_base
from spack.directives import build_system, extends
from spack.install_test import SkipTest, test_part
from spack.util.executable import Executable

from ._checks import BaseBuilder, execute_build_time_tests


class PerlPackage(spack.package_base.PackageBase):
    """Specialized class for packages that are built using Perl."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "PerlPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "perl"

    build_system("perl")

    extends("perl", when="build_system=perl")

    @property
    @memoized
    def _platform_dir(self):
        """Name of platform-specific module subdirectory."""
        perl = self.spec["perl"].command
        options = "-E", "use Config; say $Config{archname}"
        out = perl(*options, output=str.split, error=str.split)
        return out.strip()

    @property
    def use_modules(self) -> Iterable[str]:
        """Names of the package's perl modules."""
        module_files = find(self.prefix.lib, ["*.pm"], recursive=True)

        # Drop the platform directory, if present
        if self._platform_dir:
            platform_dir = self._platform_dir + os.sep
            module_files = [m.replace(platform_dir, "") for m in module_files]

        # Drop the extension and library path
        prefix = self.prefix.lib + os.sep
        modules = [os.path.splitext(m)[0].replace(prefix, "") for m in module_files]

        # Drop the perl subdirectory as well
        return ["::".join(m.split(os.sep)[1:]) for m in modules]

    @property
    def skip_modules(self) -> Iterable[str]:
        """Names of modules that should be skipped when running tests.

        These are a subset of use_modules.

        Returns:
            List of strings of module names.
        """
        return []

    def test_use(self):
        """Test 'use module'"""
        if not self.use_modules:
            raise SkipTest("Test requires use_modules package property.")

        perl = self.spec["perl"].command
        for module in self.use_modules:
            if module in self.skip_modules:
                continue

            with test_part(self, f"test_use-{module}", purpose=f"checking use of {module}"):
                options = ["-we", f'use strict; use {module}; print("OK\n")']
                out = perl(*options, output=str.split, error=str.split)
                assert "OK" in out


@spack.builder.builder("perl")
class PerlBuilder(BaseBuilder):
    """The perl builder provides four phases that can be overridden, if required:

        1. :py:meth:`~.PerlBuilder.configure`
        2. :py:meth:`~.PerlBuilder.build`
        3. :py:meth:`~.PerlBuilder.check`
        4. :py:meth:`~.PerlBuilder.install`

    The default methods use, in order of preference:
        (1) Makefile.PL,
        (2) Build.PL.

    Some packages may need to override :py:meth:`~.PerlBuilder.configure_args`,
    which produces a list of arguments for :py:meth:`~.PerlBuilder.configure`.

    Arguments should not include the installation base directory.
    """

    #: Phases of a Perl package
    phases = ("configure", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("configure_args", "check", "test_use")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ()

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    @property
    def build_method(self):
        """Searches the package for either a Makefile.PL or Build.PL.

        Raises:
            RuntimeError: if neither Makefile.PL nor Build.PL exist
        """
        if os.path.isfile("Makefile.PL"):
            build_method = "Makefile.PL"
        elif os.path.isfile("Build.PL"):
            build_method = "Build.PL"
        else:
            raise RuntimeError("Unknown build_method for perl package")
        return build_method

    @property
    def build_executable(self):
        """Returns the executable method to build the perl package"""
        if self.build_method == "Makefile.PL":
            build_executable = self.pkg.module.make
        elif self.build_method == "Build.PL":
            build_executable = Executable(os.path.join(self.pkg.stage.source_path, "Build"))
        return build_executable

    def configure_args(self):
        """List of arguments passed to :py:meth:`~.PerlBuilder.configure`.

        Arguments should not include the installation base directory, which
        is prepended automatically.
        """
        return []

    def configure(self, pkg, spec, prefix):
        """Run Makefile.PL or Build.PL with arguments consisting of
        an appropriate installation base directory followed by the
        list returned by :py:meth:`~.PerlBuilder.configure_args`.
        """
        if self.build_method == "Makefile.PL":
            options = ["Makefile.PL", "INSTALL_BASE={0}".format(prefix)]
        elif self.build_method == "Build.PL":
            options = ["Build.PL", "--install_base", prefix]
        options += self.configure_args()

        pkg.module.perl(*options)

    # It is possible that the shebang in the Build script that is created from
    # Build.PL may be too long causing the build to fail. Patching the shebang
    # does not happen until after install so set '/usr/bin/env perl' here in
    # the Build script.
    @spack.builder.run_after("configure")
    def fix_shebang(self):
        if self.build_method == "Build.PL":
            pattern = "#!{0}".format(self.spec["perl"].command.path)
            repl = "#!/usr/bin/env perl"
            filter_file(pattern, repl, "Build", backup=False)

    def build(self, pkg, spec, prefix):
        """Builds a Perl package."""
        self.build_executable()

    # Ensure that tests run after build (if requested):
    spack.builder.run_after("build")(execute_build_time_tests)

    def check(self):
        """Runs built-in tests of a Perl package."""
        self.build_executable("test")

    def install(self, pkg, spec, prefix):
        """Installs a Perl package."""
        self.build_executable("install")
