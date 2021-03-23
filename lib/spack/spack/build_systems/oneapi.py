# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Common utilities for managing intel oneapi packages.

"""

from sys import platform
from os.path import basename, dirname, isdir, join

from spack.package import Package
from spack.util.environment import EnvironmentModifications
from spack.util.executable import Executable

from llnl.util.filesystem import find_headers, find_libraries


class IntelOneApiPackage(Package):
    """Base class for Intel oneAPI packages."""

    homepage = 'https://software.intel.com/oneapi'

    phases = ['install']

    # oneAPI license does not allow mirroring outside of the
    # organization (e.g. University/Company).
    redistribute_source = False

    @property
    def component_dir(self):
        """Subdirectory for this component in the install prefix."""
        raise NotImplementedError

    def install(self, spec, prefix, installer_path=None):
        """Shared install method for all oneapi packages."""

        # intel-oneapi-compilers overrides the installer_path when
        # installing fortran, which comes from a spack resource
        if installer_path is None:
            installer_path = basename(self.url_for_version(spec.version))

        if platform == 'linux':
            bash = Executable('bash')

            # Installer writes files in ~/intel set HOME so it goes to prefix
            bash.add_default_env('HOME', prefix)

            bash(installer_path,
                 '-s', '-a', '-s', '--action', 'install',
                 '--eula', 'accept',
                 '--install-dir', prefix)

        # Some installers have a bug and do not return an error code when failing
        if not isdir(join(prefix, self.component_dir)):
            raise RuntimeError('install failed')

    def setup_run_environment(self, env):

        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/setvars.sh --force
        """
        env.extend(EnvironmentModifications.from_sourcing_file(
            join(self.prefix, self.component_dir, 'latest/env/vars.sh')))


class IntelOneApiLibraryPackage(IntelOneApiPackage):
    """Base class for Intel oneAPI library packages."""

    @property
    def headers(self):
        include_path = '%s/%s/latest/include' % (
            self.prefix, self.component_dir)
        return find_headers('*', include_path, recursive=True)

    @property
    def libs(self):
        lib_path = '%s/%s/latest/lib/intel64' % (self.prefix, self.component_dir)
        lib_path = lib_path if isdir(lib_path) else dirname(lib_path)
        return find_libraries('*', root=lib_path, shared=True, recursive=True)
