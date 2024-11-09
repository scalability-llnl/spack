# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.filesystem as fs

import spack.builder
import spack.package_base
from spack.directives import build_system, depends_on
from spack.multimethod import when

from ._checks import BaseBuilder, execute_install_time_tests


class CargoPackage(spack.package_base.PackageBase):
    """Specialized class for packages built using cargo."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "CargoPackage"

    build_system("cargo")

    with when("build_system=cargo"):
        depends_on("rust", type="build")


@spack.builder.builder("cargo")
class CargoBuilder(BaseBuilder):
    """The Cargo builder encodes the most common way of building software with
    a rust Cargo.toml file. It has two phases that can be overridden, if need be:

            1. :py:meth:`~.CargoBuilder.build`
            2. :py:meth:`~.CargoBuilder.install`

    For a finer tuning you may override:

        +-----------------------------------------------+----------------------+
        | **Method**                                    | **Purpose**          |
        +===============================================+======================+
        | :py:meth:`~.CargoBuilder.build_args`          | Specify arguments    |
        |                                               | to ``cargo install`` |
        +-----------------------------------------------+----------------------+
        | :py:meth:`~.CargoBuilder.check_args`          | Specify arguments    |
        |                                               | to ``cargo test``    |
        +-----------------------------------------------+----------------------+
    """

    phases = ("build", "install")

    #: Callback names for install-time test
    install_time_test_callbacks = ["check"]

    @property
    def build_directory(self):
        """Return the directory containing the main Cargo.toml."""
        return self.pkg.stage.source_path

    @property
    def build_args(self):
        """Arguments for ``cargo build``."""
        return []

    @property
    def check_args(self):
        """Argument for ``cargo test`` during check phase"""
        return []

    def build(self, pkg, spec, prefix):
        """Runs ``cargo install`` in the source directory"""
        with fs.working_dir(self.build_directory):
            pkg.module.cargo("install", "--root", "out", "--path", ".", *self.build_args)

    def install(self, pkg, spec, prefix):
        """Copy build files into package prefix."""
        with fs.working_dir(self.build_directory):
            fs.install_tree("out", prefix)

    spack.builder.run_after("install")(execute_install_time_tests)

    def check(self):
        """Run "cargo test"."""
        with fs.working_dir(self.build_directory):
            self.pkg.module.cargo("test", *self.check_args)
