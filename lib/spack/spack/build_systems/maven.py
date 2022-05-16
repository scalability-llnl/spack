# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util.filesystem import install_tree, working_dir

import spack.builder
import spack.package
from spack.directives import buildsystem, depends_on
from spack.multimethod import when
from spack.util.executable import which

maven = spack.builder.BuilderMeta.make_decorator('maven')


class MavenPackage(spack.package.PackageBase):
    """Specialized class for packages that are built using the
    Maven build system. See https://maven.apache.org/index.html
    for more information.

    This class provides the following phases that can be overridden:

    * build
    * install
    """
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'MavenPackage'

    buildsystem('maven')
    with when('buildsystem=maven'):
        depends_on('java', type=('build', 'run'))
        depends_on('maven', type='build')


@spack.builder.builder('maven')
class MavenBuilder(spack.builder.Builder):
    phases = ('build', 'install')

    class PackageWrapper(spack.builder.BuildWrapper):
        @property
        def build_directory(self):
            """The directory containing the ``pom.xml`` file."""
            return self.stage.source_path

        def build_args(self):
            """List of args to pass to build phase."""
            return []

        def build(self, spec, prefix):
            """Compile code and package into a JAR file."""

            with working_dir(self.build_directory):
                mvn = which('mvn')
                if self.run_tests:
                    mvn('verify', *self.build_args())
                else:
                    mvn('package', '-DskipTests', *self.build_args())

        def install(self, spec, prefix):
            """Copy to installation prefix."""

            with working_dir(self.build_directory):
                install_tree('.', prefix)

        # Check that self.prefix is there after installation
        maven.run_after('install')(spack.package.PackageBase.sanity_check_prefix)
