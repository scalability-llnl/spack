# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect

from spack.directives import depends_on, extends
from spack.package_base import PackageBase, run_after


class RPackage(PackageBase):
    """Specialized class for packages that are built using R.

    For more information on the R build system, see:
    https://stat.ethz.ch/R-manual/R-devel/library/utils/html/INSTALL.html

    This class provides a single phase that can be overridden:

        1. :py:meth:`~.RPackage.install`

    It has sensible defaults, and for many packages the only thing
    necessary will be to add dependencies
    """
    phases = ['install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'RPackage'

    extends('r')

    depends_on('r', type=('build', 'run'))

    def configure_args(self):
        """Arguments to pass to install via ``--configure-args``."""
        return []

    def configure_vars(self):
        """Arguments to pass to install via ``--configure-vars``."""
        return []

    def install(self, spec, prefix):
        """Installs an R package."""

        config_args = self.configure_args()
        config_vars = self.configure_vars()

        args = [
            'CMD',
            'INSTALL'
        ]

        if config_args:
            args.append('--configure-args={0}'.format(' '.join(config_args)))

        if config_vars:
            args.append('--configure-vars={0}'.format(' '.join(config_vars)))

        args.extend([
            '--library={0}'.format(self.module.r_lib_dir),
            self.stage.source_path
        ])

        inspect.getmodule(self).R(*args)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
