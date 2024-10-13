# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob

import spack.builder
import spack.package_base
from spack.directives import build_system, extends, maintainers

from ._checks import BaseBuilder


class RubyPackage(spack.package_base.PackageBase):
    """Specialized class for building Ruby gems."""

    maintainers("Kerilk")

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "RubyPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "ruby"

    build_system("ruby")

    extends("ruby", when="build_system=ruby")


@spack.builder.builder("ruby")
class RubyBuilder(BaseBuilder):
    """The Ruby builder provides two phases that can be overridden if required:

    #. :py:meth:`~.RubyBuilder.build`
    #. :py:meth:`~.RubyBuilder.install`
    """

    phases = ("build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ()

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ()

    def build(self, pkg, spec, prefix):
        """Build a Ruby gem."""

        # ruby-rake provides both rake.gemspec and Rakefile, but only
        # rake.gemspec can be built without an existing rake installation
        gemspecs = glob.glob("*.gemspec")
        rakefiles = glob.glob("Rakefile")
        if gemspecs:
            pkg.module.gem("build", "--norc", gemspecs[0])
        elif rakefiles:
            jobs = pkg.module.make_jobs
            pkg.module.rake("package", "-j{0}".format(jobs))
        else:
            # Some Ruby packages only ship `*.gem` files, so nothing to build
            pass

    def install(self, pkg, spec, prefix):
        """Install a Ruby gem.

        The ruby package sets ``GEM_HOME`` to tell gem where to install to."""

        gems = glob.glob("*.gem")
        if gems:
            # if --install-dir is not used, GEM_PATH is deleted from the
            # environement, and Gems required to build native extensions will
            # not be found. Those extensions are built during `gem install`.
            pkg.module.gem(
                "install", "--norc", "--ignore-dependencies", "--install-dir", prefix, gems[0]
            )
