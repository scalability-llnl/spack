# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.filesystem as fs

import spack.builder
import spack.package_base
import spack.spec
import spack.util.prefix
from spack.directives import build_system, depends_on
from spack.multimethod import when
from spack.util.executable import which

from ._checks import BuilderWithDefaults


class MavenPackage(spack.package_base.PackageBase):
    """Specialized class for packages that are built using the
    Maven build system. See https://maven.apache.org/index.html
    for more information.
    """

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "MavenPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "maven"

    build_system("maven")

    with when("build_system=maven"):
        depends_on("java", type=("build", "run"))
        depends_on("maven", type="build")


@spack.builder.builder("maven")
class MavenBuilder(BuilderWithDefaults):
    """The Maven builder encodes the default way to build software with Maven.
    It has two phases that can be overridden, if need be:

        1. :py:meth:`~.MavenBuilder.build`
        2. :py:meth:`~.MavenBuilder.install`
    """

    phases = ("build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("build_args",)

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ("build_directory",)

    @property
    def build_directory(self):
        """The directory containing the ``pom.xml`` file."""
        return self.pkg.stage.source_path

    def build_args(self):
        """List of args to pass to build phase."""
        return []

    def build(
        self, pkg: MavenPackage, spec: spack.spec.Spec, prefix: spack.util.prefix.Prefix
    ) -> None:
        """Compile code and package into a JAR file."""
        with fs.working_dir(self.build_directory):
            mvn = which("mvn", required=True)
            if self.pkg.run_tests:
                mvn("verify", *self.build_args())
            else:
                mvn("package", "-DskipTests", *self.build_args())

    def install(
        self, pkg: MavenPackage, spec: spack.spec.Spec, prefix: spack.util.prefix.Prefix
    ) -> None:
        """Copy to installation prefix."""
        with fs.working_dir(self.build_directory):
            fs.install_tree(".", prefix)
