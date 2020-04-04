# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from llnl.util.filesystem import mkdirp, install
from spack.directives import depends_on
from spack.package import PackageBase, run_after
from spack.util.executable import Executable


class GoPackage(PackageBase):
    """Specialized class for packages that are built using Go.

    This class provides two phases that can be overridden if required:

        1. :py:meth:`~.GoPackage.build`
        2. :py:meth:`~.GoPackage.install`

    Packages must add the binaries to installed to
    :py:attr:`~.GoPackage.executables`.

    Additional build flags can be added to
    :py:attr:`~.GoPackage.build_flags`.

    :py:meth:`~.GoPackage.setup_build_environment` sets
    ``GO111MODULE=on`` to enable module mode and sets
    ``GOFLAGS=-mod=vendor`` to enable vendoring and prevent ``go``
    from downloading libraries at build time.
    """

    #: Phases of a Go package
    phases = ['build', 'install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'GoPackage'

    depends_on('go@1.11:', type=('build'))

    go = Executable('go')
    executables = []

    def setup_build_environment(self, env):
        # Set it, it's either on or off, and we want it *on*.
        env.set('GO111MODULE', 'on')

    def build(self, spec, prefix):
        """Builds a Go package."""
        args = self.build_args()

        self.go('build', '-mod=vendor', *args)

    def build_args(self):
        """Arguments to pass to build."""
        return []

    def install(self, spec, prefix):
        """Installs a Go package."""
        if len(self.executables) == 0:
            raise Exception('Nothing to install, ' +
                            'executables may not be an empty list')
        mkdirp(prefix.bin)
        for f in self.executables:
            install(f, prefix.bin)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
