# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.builder
import spack.package_base
from spack.directives import build_system, extends
from spack.multimethod import when

from ._checks import BaseBuilder


class OctavePackage(spack.package_base.PackageBase):
    """Specialized class for Octave packages. See
    https://www.gnu.org/software/octave/doc/v4.2.0/Installing-and-Removing-Packages.html
    for more information.
    """

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "OctavePackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "octave"

    build_system("octave")

    with when("build_system=octave"):
        extends("octave")


@spack.builder.builder("octave")
class OctaveBuilder(BaseBuilder):
    """The octave builder provides the following phases that can be overridden:

    1. :py:meth:`~.OctaveBuilder.install`
    """

    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    legacy_methods = ()

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ()

    def install(self, pkg, spec, prefix):
        """Install the package from the archive file"""
        pkg.module.octave(
            "--quiet",
            "--norc",
            "--built-in-docstrings-file=/dev/null",
            "--texi-macros-file=/dev/null",
            "--eval",
            "pkg prefix %s; pkg install %s" % (prefix, self.pkg.stage.archive_file),
        )

    def setup_build_environment(self, env):
        # octave does not like those environment variables to be set:
        env.unset("CC")
        env.unset("CXX")
        env.unset("FC")
