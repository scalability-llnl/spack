# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Genometools(MakefilePackage):
    """genometools is a free collection of bioinformatics tools (in the realm
       of genome informatics) combined into a single binary named gt."""

    homepage = "http://genometools.org/"
    url      = "https://github.com/genometools/genometools/archive/v1.6.1.tar.gz"

    version('1.6.1', sha256='528ca143a7f1d42af8614d60ea1e5518012913a23526d82e434f0dad2e2d863f')
    version('1.5.9', sha256='bba8e043f097e7c72e823f73cb0efbd20bbd60f1ce797a0e4c0ab632b170c909')

    depends_on('perl', type=('build', 'run'))
    depends_on('cairo+pdf')
    depends_on('pango')

    # build fails with gcc 7"
    conflicts('%gcc@7.1.0:', when='@:1.5.9')

    patch('signed.patch', when='%fj')

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('CPATH', self.prefix.include.genometools)
