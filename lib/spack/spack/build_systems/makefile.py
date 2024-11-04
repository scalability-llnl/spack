# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

import llnl.util.filesystem as fs

import spack.builder
import spack.package_base
from spack.directives import build_system, conflicts, depends_on
from spack.multimethod import when

from ._checks import (
    BaseBuilder,
    apply_macos_rpath_fixups,
    execute_build_time_tests,
    execute_install_time_tests,
)


class MakefilePackage(spack.package_base.PackageBase):
    """Specialized class for packages built using Makefiles."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "MakefilePackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "makefile"

    build_system("makefile")

    with when("build_system=makefile"):
        conflicts("platform=windows")
        depends_on("gmake", type="build")


@spack.builder.builder("makefile")
class MakefileBuilder(BaseBuilder):
    """The Makefile builder encodes the most common way of building software with
    Makefiles. It has three phases that can be overridden, if need be:

            1. :py:meth:`~.MakefileBuilder.edit`
            2. :py:meth:`~.MakefileBuilder.build`
            3. :py:meth:`~.MakefileBuilder.install`

    It is usually necessary to override the :py:meth:`~.MakefileBuilder.edit`
    phase (which is by default a no-op), while the other two have sensible defaults.

    For a finer tuning you may override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:attr:`~.MakefileBuilder.build_targets`    | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | build phase        |
        +-----------------------------------------------+--------------------+
        | :py:attr:`~.MakefileBuilder.install_targets`  | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | install phase      |
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.MakefileBuilder.build_directory`  | Directory where the|
        |                                               | Makefile is located|
        +-----------------------------------------------+--------------------+
    """

    phases = ("edit", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("check", "installcheck")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = (
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "install_time_test_callbacks",
        "build_directory",
    )

    #: Targets for ``make`` during the :py:meth:`~.MakefileBuilder.build` phase
    build_targets: List[str] = []
    #: Targets for ``make`` during the :py:meth:`~.MakefileBuilder.install` phase
    install_targets = ["install"]

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    #: Callback names for install-time test
    install_time_test_callbacks = ["installcheck"]

    @property
    def build_directory(self):
        """Return the directory containing the main Makefile."""
        return self.pkg.stage.source_path

    def edit(self, pkg, spec, prefix):
        """Edit the Makefile before calling make. The default is a no-op."""
        pass

    def build(self, pkg, spec, prefix):
        """Run "make" on the build targets specified by the builder."""
        with fs.working_dir(self.build_directory):
            pkg.module.make(*self.build_targets)

    def install(self, pkg, spec, prefix):
        """Run "make" on the install targets specified by the builder."""
        with fs.working_dir(self.build_directory):
            pkg.module.make(*self.install_targets)

    spack.builder.run_after("build")(execute_build_time_tests)

    def check(self):
        """Run "make" on the ``test`` and ``check`` targets, if found."""
        with fs.working_dir(self.build_directory):
            self.pkg._if_make_target_execute("test")
            self.pkg._if_make_target_execute("check")

    spack.builder.run_after("install")(execute_install_time_tests)

    def installcheck(self):
        """Searches the Makefile for an ``installcheck`` target
        and runs it if found.
        """
        with fs.working_dir(self.build_directory):
            self.pkg._if_make_target_execute("installcheck")

    # On macOS, force rpaths for shared library IDs and remove duplicate rpaths
    spack.builder.run_after("install", when="platform=darwin")(apply_macos_rpath_fixups)
