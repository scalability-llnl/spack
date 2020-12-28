# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opium(AutotoolsPackage):
    """DFT pseudopotential generation project"""

    homepage = "https://opium.sourceforge.net/index.html"
    url = "https://downloads.sourceforge.net/project/opium/opium/opium-v3.8/opium-v3.8-src.tgz"

    version('3.8', sha256='edee6606519330aecaee436ee8cfb0a33788b5677861d59e38aba936e87d5ad3')

    depends_on('blas')
    depends_on('lapack')

    def configure_args(self):
        spec = self.spec
        options = []
        libs = spec['lapack'].libs + spec['blas'].libs
        options.append('LDFLAGS=%s' % libs.ld_flags)
        return options

    def build(self, spec, prefix):
        with working_dir("src", create=False):
            make("all-subdirs")
            make("opium")

    def install(self, spec, prefix):
        # opium not have a make install :-((
        mkdirp(self.prefix.bin)
        install(join_path(self.stage.source_path, 'opium'),
                self.prefix.bin)
