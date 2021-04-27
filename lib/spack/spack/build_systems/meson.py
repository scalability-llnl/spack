# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect
import os
from typing import List  # novm

from llnl.util.filesystem import working_dir
from spack.directives import depends_on, variant
from spack.package import PackageBase, run_after


class MesonPackage(PackageBase):
    """Specialized class for packages built using Meson

    For more information on the Meson build system, see:
    https://mesonbuild.com/

    This class provides three phases that can be overridden:

        1. :py:meth:`~.MesonPackage.meson`
        2. :py:meth:`~.MesonPackage.build`
        3. :py:meth:`~.MesonPackage.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.MesonPackage.meson_args`.
    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:meth:`~.MesonPackage.root_mesonlists_dir` | Location of the    |
        |                                               | root MesonLists.txt|
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.MesonPackage.build_directory`     | Directory where to |
        |                                               | build the package  |
        +-----------------------------------------------+--------------------+


    """
    #: Phases of a Meson package
    phases = ['meson', 'build', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'MesonPackage'

    build_targets = []  # type: List[str]
    install_targets = ['install']

    build_time_test_callbacks = ['check']

    variant('buildtype', default='debugoptimized',
            description='Meson build type',
            values=('plain', 'debug', 'debugoptimized', 'release', 'minsize'))
    variant('default_library', default='shared',
            description=' Default library type',
            values=('shared', 'static', 'both'))
    variant('strip', default=False, description='Strip targets on install')

    depends_on('meson', type='build')
    depends_on('ninja', type='build')

    @property
    def archive_files(self):
        """Files to archive for packages based on Meson"""
        return [os.path.join(self.build_directory, 'meson-logs/meson-log.txt')]

    @property
    def root_mesonlists_dir(self):
        """The relative path to the directory containing meson.build

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing meson.build
        """
        return self.stage.source_path

    @property
    def std_meson_args(self):
        """Standard meson arguments provided as a property for
        convenience of package writers

        :return: standard meson arguments
        """
        # standard Meson arguments
        std_meson_args = MesonPackage._std_args(self)
        std_meson_args += getattr(self, 'meson_flag_args', [])
        return std_meson_args

    @staticmethod
    def _std_args(pkg):
        """Computes the standard meson arguments for a generic package"""

        try:
            build_type = pkg.spec.variants['buildtype'].value
        except KeyError:
            build_type = 'release'

        strip = 'true' if '+strip' in pkg.spec else 'false'

        try:
            default_library = pkg.spec.variants['default_library'].value
        except KeyError:
            default_library = 'shared'

        args = [
            '--prefix={0}'.format(pkg.prefix),
            # If we do not specify libdir explicitly, Meson chooses something
            # like lib/x86_64-linux-gnu, which causes problems when trying to
            # find libraries and pkg-config files.
            # See https://github.com/mesonbuild/meson/issues/2197
            '--libdir={0}'.format(pkg.prefix.lib),
            '-Dbuildtype={0}'.format(build_type),
            '-Dstrip={0}'.format(strip),
            '-Ddefault_library={0}'.format(default_library)
        ]

        return args

    def flags_to_build_system_args(self, flags):
        """Produces a list of all command line arguments to pass the specified
        compiler flags to meson."""
        # Has to be dynamic attribute due to caching
        setattr(self, 'meson_flag_args', [])

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return os.path.join(self.stage.source_path, 'spack-build')

    def meson_args(self):
        """Produces a list containing all the arguments that must be passed to
        meson, except:

        * ``--prefix``
        * ``--libdir``
        * ``--buildtype``
        * ``--strip``
        * ``--default_library``

        which will be set automatically.

        :return: list of arguments for meson
        """
        return []

    def meson(self, spec, prefix):
        """Runs ``meson`` in the build directory"""
        options = [os.path.abspath(self.root_mesonlists_dir)]
        options += self.std_meson_args
        options += self.meson_args()
        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).meson(*options)

    def build(self, spec, prefix):
        """Make the build targets"""
        options = ['-v']
        options += self.build_targets
        with working_dir(self.build_directory):
            inspect.getmodule(self).ninja(*options)

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            inspect.getmodule(self).ninja(*self.install_targets)

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    def check(self):
        """Searches the Meson-generated file for the target ``test``
        and runs it if found.
        """
        with working_dir(self.build_directory):
            self._if_ninja_target_execute('test')
            self._if_ninja_target_execute('check')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
