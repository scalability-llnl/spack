# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util.filesystem import working_dir

import spack.builder
import spack.package_base
from spack.directives import build_system, depends_on

from ._checks import BaseBuilder, execute_build_time_tests


class QMakePackage(spack.package_base.PackageBase):
    """Specialized class for packages built using qmake.

    For more information on the qmake build system, see:
    http://doc.qt.io/qt-5/qmake-manual.html
    """

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "QMakePackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "qmake"

    build_system("qmake")

    depends_on("qmake", type="build", when="build_system=qmake")


@spack.builder.builder("qmake")
class QMakeBuilder(BaseBuilder):
    """The qmake builder provides three phases that can be overridden:

    1. :py:meth:`~.QMakeBuilder.qmake`
    2. :py:meth:`~.QMakeBuilder.build`
    3. :py:meth:`~.QMakeBuilder.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.QMakeBuilder.qmake_args`.
    """

    phases = ("qmake", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("qmake_args", "check")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ("build_directory", "build_time_test_callbacks")

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    @property
    def build_directory(self):
        """The directory containing the ``*.pro`` file."""
        return self.stage.source_path

    def qmake_args(self):
        """List of arguments passed to qmake."""
        return []

    def qmake(self, pkg, spec, prefix):
        """Run ``qmake`` to configure the project and generate a Makefile."""
        with working_dir(self.build_directory):
            pkg.module.qmake(*self.qmake_args())

    def build(self, pkg, spec, prefix):
        """Make the build targets"""
        with working_dir(self.build_directory):
            pkg.module.make()

    def install(self, pkg, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            pkg.module.make("install")

    def check(self):
        """Search the Makefile for a ``check:`` target and runs it if found."""
        with working_dir(self.build_directory):
            self.pkg._if_make_target_execute("check")

    spack.builder.run_after("build")(execute_build_time_tests)
