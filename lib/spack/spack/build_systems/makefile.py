# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect
from typing import List  # novm

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir
from spack.package_base import PackageBase, run_after


class MakefilePackage(PackageBase):
    """Specialized class for packages that are built using editable Makefiles

    This class provides three phases that can be overridden:

        1. :py:meth:`~.MakefilePackage.edit`
        2. :py:meth:`~.MakefilePackage.build`
        3. :py:meth:`~.MakefilePackage.install`

    It is usually necessary to override the :py:meth:`~.MakefilePackage.edit`
    phase, while :py:meth:`~.MakefilePackage.build` and
    :py:meth:`~.MakefilePackage.install` have sensible defaults.
    For a finer tuning you may override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:attr:`~.MakefilePackage.build_targets`    | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | build phase        |
        +-----------------------------------------------+--------------------+
        | :py:attr:`~.MakefilePackage.install_targets`  | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | install phase      |
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.MakefilePackage.build_directory`  | Directory where the|
        |                                               | Makefile is located|
        +-----------------------------------------------+--------------------+
    """
    #: Phases of a package that is built with an hand-written Makefile
    phases = ['edit', 'build', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'MakefilePackage'

    #: Targets for ``make`` during the :py:meth:`~.MakefilePackage.build`
    #: phase
    build_targets = []  # type: List[str]
    #: Targets for ``make`` during the :py:meth:`~.MakefilePackage.install`
    #: phase
    install_targets = ['install']

    #: Callback names for build-time test
    build_time_test_callbacks = ['check']

    #: Callback names for install-time test
    install_time_test_callbacks = ['installcheck']

    @property
    def build_directory(self):
        """Returns the directory containing the main Makefile

        :return: build directory
        """
        return self.stage.source_path

    def edit(self, spec, prefix):
        """Edits the Makefile before calling make. This phase cannot
        be defaulted.
        """
        tty.msg('Using default implementation: skipping edit phase.')

    def build(self, spec, prefix):
        """Calls make, passing :py:attr:`~.MakefilePackage.build_targets`
        as targets.
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        """Calls make, passing :py:attr:`~.MakefilePackage.install_targets`
        as targets.
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.install_targets)

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    def check(self):
        """Searches the Makefile for targets ``test`` and ``check``
        and runs them if found.
        """
        with working_dir(self.build_directory):
            self._if_make_target_execute('test')
            self._if_make_target_execute('check')

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    def installcheck(self):
        """Searches the Makefile for an ``installcheck`` target
        and runs it if found.
        """
        with working_dir(self.build_directory):
            self._if_make_target_execute('installcheck')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
