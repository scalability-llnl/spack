# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EaUtils(MakefilePackage):
    """Command-line tools for processing biological sequencing data. Barcode
       demultiplexing, adapter trimming, etc. Primarily written to support an
       Illumina based pipeline - but should work with any FASTQs."""

    homepage = "http://expressionanalysis.github.io/ea-utils/"
    url = "https://github.com/ExpressionAnalysis/ea-utils/archive/1.04.807.tar.gz"

    version('1.04.807', sha256='aa09d25e6aa7ae71d2ce4198a98e58d563f151f8ff248e4602fa437f12b8d05f')

    depends_on('subversion')
    depends_on('zlib')
    depends_on('gsl')
    depends_on('bamtools')
    # perl module required for make check, which is included in the default
    # target
    depends_on('perl', type='build')

    build_directory = 'clipper'

    def edit(self, spec, prefix):
        with working_dir('clipper'):
            makefile = FileFilter('Makefile')
            makefile.filter('/usr', prefix)
