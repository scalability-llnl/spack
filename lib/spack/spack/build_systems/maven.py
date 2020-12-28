# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from llnl.util.filesystem import install_tree, working_dir
from spack.directives import depends_on
from spack.package_base import PackageBase, run_after
from spack.util.executable import which


class MavenPackage(PackageBase):
    """Specialized class for packages that are built using the
    Maven build system. See https://maven.apache.org/index.html
    for more information.

    This class provides the following phases that can be overridden:

    * build
    * install
    """
    # Default phases
    phases = ['build', 'install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'MavenPackage'

    depends_on('java', type=('build', 'run'))
    depends_on('maven', type='build')

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
    run_after('install')(PackageBase.sanity_check_prefix)
