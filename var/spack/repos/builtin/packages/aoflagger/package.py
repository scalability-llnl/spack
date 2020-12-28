# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aoflagger(CMakePackage):
    """RFI detector and quality analysis
    for astronomical radio observations."""

    homepage = "https://sourceforge.net/projects/aoflagger/"
    url      = "https://downloads.sourceforge.net/project/aoflagger/aoflagger-2.10.0/aoflagger-2.10.0.tar.bz2"

    version('2.10.0', sha256='3ec1188d37101acf2029575ebc09c50b19c158c88a12b55ac5d25a96bd8fc18d')

    depends_on('casacore+python+fftw@1.9.99:')
    depends_on('fftw~mpi@3.0:')
    depends_on('boost+python@:1.66.99')
    depends_on('libxml2')
    depends_on('lapack')
    depends_on('cfitsio')
