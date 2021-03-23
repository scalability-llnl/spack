# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Delly2(MakefilePackage):
    """Delly2 is an integrated structural variant prediction method that can
       discover, genotype and visualize deletions, tandem duplications,
       inversions and translocations at single-nucleotide resolution in
       short-read massively parallel sequencing data.."""

    homepage = "https://github.com/dellytools/delly"
    git      = "https://github.com/dellytools/delly.git"

    version('2017-08-03', commit='e32a9cd55c7e3df5a6ae4a91f31a0deb354529fc')

    depends_on('htslib')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('bcftools')

    def edit(self, spec, prefix):
        # Only want to build delly source, not submodules. Build fails
        # using provided submodules, succeeds with existing spack recipes.
        makefile = FileFilter('Makefile')
        makefile.filter('HTSLIBSOURCES =', '#HTSLIBSOURCES')
        makefile.filter('BOOSTSOURCES =', '#BOOSTSOURCES')
        makefile.filter('SEQTK_ROOT ?=', '#SEQTK_ROOT')
        makefile.filter('BOOST_ROOT ?=', '#BOOST_ROOT')
        makefile.filter('cd src', '# cd src')
        makefile.filter('.htslib ', '')
        makefile.filter('.bcftools ', '')
        makefile.filter('.boost ', '')
        makefile.filter('.htslib:', '# .htslib:')
        makefile.filter('.bcftools:', '# .bcftools:')
        makefile.filter('.boost:', '# .boost:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('src'):
            install('delly', prefix.bin)
            install('dpe', prefix.bin)
            install('cov', prefix.bin)
