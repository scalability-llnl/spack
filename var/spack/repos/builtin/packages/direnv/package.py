# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os.path

from spack import *


class Direnv(Package):
    """direnv is an environment switcher for the shell."""

    homepage = "https://direnv.net/"
    url      = "https://github.com/direnv/direnv/archive/v2.11.3.tar.gz"

    version('2.20.0', sha256='cc72525b0a5b3c2ab9a52a3696e95562913cd431f923bcc967591e75b7541bff')
    version('2.11.3', sha256='2d34103a7f9645059270763a0cfe82085f6d9fe61b2a85aca558689df0e7b006')

    depends_on('go@1.11:', type='build')  # module/vendor support
    depends_on('gmake')  # project uses a GNUmakefile

    # It takes a bit of sneaky to avoid downloading things at build time...
    # There's a vendor dir, but using it is tricksy (it dates from
    # go's early days...)
    # - set the appropriate environment variables so the current
    #   compilers (@1.11:) use module mode
    # - drop an otherwise useless go.mod so that the compiler
    #   is willing to enter module mode
    # - remove some bits of the GNUmakefile in @2.20.0 that get in
    #   the way

    def setup_build_environment(self, env):
        # forcibly enable module mode
        env.set('GO111MODULE', 'on')
        # forcibly enable vendoring, prevent network access
        env.set('GOFLAGS', '-mod=vendor')

    @run_before('install')
    def install_go_mod(self):
        # cribbed from wannier90
        go_mod = join_path(
            os.path.dirname(inspect.getmodule(self).__file__), 'go.mod')
        copy(go_mod, 'go.mod')

    @run_before('install')
    def edit_makefile(self):
        if self.spec.satisfies('@2.20.0'):
            makefile = FileFilter('GNUmakefile')
            makefile.filter('direnv: stdlib.go *.go | $(base)',
                            'direnv: stdlib.go *.go', string=True)
            makefile.filter(
                'cd "$(base)" && $(GO) build $(GO_FLAGS) -o $(exe)',
                '$(GO) build $(GO_FLAGS) -o $(exe)', string=True)

    def install(self, spec, prefix):
        make('install', "DESTDIR=%s" % prefix)
