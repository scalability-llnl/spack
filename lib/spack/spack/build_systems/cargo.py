# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.filesystem as fs

import spack.builder
import spack.package_base
import spack.phase_callbacks
import spack.spec
import spack.util.prefix
from spack.directives import build_system, depends_on
from spack.multimethod import when

from ._checks import BuilderWithDefaults, execute_install_time_tests


class CargoPackage(spack.package_base.PackageBase):
    """Specialized class for packages built using cargo."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "CargoPackage"

    build_system("cargo")

    with when("build_system=cargo"):
        depends_on("rust", type="build")


@spack.builder.builder("cargo")
class CargoBuilder(BuilderWithDefaults):
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

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("check", "installcheck")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = (
        "build_args",
        "check_args",
        "build_directory",
        "install_time_test_callbacks",
    )

    #: Callback names for install-time test
    install_time_test_callbacks = ["check"]

    @property
    def build_directory(self):
        """Return the directory containing the main Cargo.toml."""
        return self.pkg.stage.source_path

    @property
    def build_args(self):
        """Arguments for ``cargo build``."""
        return ["-j", str(self.pkg.module.make_jobs)]

    @property
    def check_args(self):
        """Argument for ``cargo test`` during check phase"""
        return []

    def setup_build_environment(self, env):
        env.set("CARGO_HOME", self.stage.path)

    def build(
        self, pkg: CargoPackage, spec: spack.spec.Spec, prefix: spack.util.prefix.Prefix
    ) -> None:
        """Runs ``cargo install`` in the source directory"""
        with fs.working_dir(self.build_directory):
            pkg.module.cargo("install", "--root", "out", "--path", ".", *self.build_args)

    def install(
        self, pkg: CargoPackage, spec: spack.spec.Spec, prefix: spack.util.prefix.Prefix
    ) -> None:
        """Copy build files into package prefix."""
        with fs.working_dir(self.build_directory):
            fs.install_tree("out", prefix)

    spack.phase_callbacks.run_after("install")(execute_install_time_tests)

    def check(self):
        """Run "cargo test"."""
        with fs.working_dir(self.build_directory):
            self.pkg.module.cargo("test", *self.check_args)
