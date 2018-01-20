##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Xhmm(MakefilePackage):
    """The XHMM C++ software suite was written to
    call copy number variation (CNV) from next-generation
    sequencing projects, where exome capture was used
    (or targeted sequencing, more generally)."""

    homepage = "http://atgu.mgh.harvard.edu/xhmm/index.shtml"
    url      = "https://bitbucket.org/statgen/xhmm.git"

    version('20160104', git='https://bitbucket.org/statgen/xhmm.git',
            commit='cc14e528d90932f059ac4fe94e869e81221fd732')

    depends_on('lapack')

    def edit(self, spec, prefix):
        makefile = FileFilter('sources/hmm++/config_rules.Makefile')
        makefile.filter('GCC', 'CC')
        makefile.filter('GCC =gcc', '')

    def build(self, spec, prefix):
        # TODO: Add more BLAS libs
        if '^openblas' in spec:
            lapacklib = 'openblas'
        make('LAPACK_LIBS=%s' % lapacklib)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('xhmm', prefix.bin)
