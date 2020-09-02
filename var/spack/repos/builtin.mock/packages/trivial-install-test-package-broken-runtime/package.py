# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TrivialInstallTestPackageBrokenRuntime(Package):
    """This package is a stub with a trivial install method.  It allows us
       to test the install and uninstall logic of spack."""
    homepage = "http://www.example.com/trivial_install"
    url      = "http://www.unit-test-should-replace-this-url/trivial_install-1.0.tar.gz"

    version('1.0', 'foobarbaz')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make('install')

    def setup_run_environment(self, spec):
        raise RuntimeError("runtime setup had issues!")
