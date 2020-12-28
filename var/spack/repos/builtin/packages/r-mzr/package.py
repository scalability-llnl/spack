# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMzr(RPackage):
    """parser for netCDF, mzXML, mzData and mzML and mzIdentML files (mass
       spectrometry data).

       mzR provides a unified API to the common file formats and parsers
       available for mass spectrometry data. It comes with a wrapper for the
       ISB random access parser for mass spectrometry mzXML, mzData and mzML
       files. The package contains the original code written by the ISB, and a
       subset of the proteowizard library for mzML and mzIdentML. The netCDF
       reading code has previously been used in XCMS."""

    homepage = "https://bioconductor.org/packages/mzR"
    git      = "https://git.bioconductor.org/packages/mzR.git"

    version('2.18.1', commit='13f9f9b1149859c3e29cfce941d958cc4f680546')
    version('2.16.2', commit='22d7dad98f46b5bed7f6f7b3a703dcdf5997f709')
    version('2.14.0', commit='bf1154bc45101d95b5a67c66980856a779b84bd4')
    version('2.12.0', commit='f05eb27ae31c3d019cca10fc3b9ee513cbcdfc5a')
    version('2.10.0', commit='a6168b68e48c281e88de9647254a8db1e21df388')

    depends_on('r-rcpp@0.10.1:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics@0.13.6:', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))

    depends_on('r-protgenerics@1.9.1:', when='@2.12.0:', type=('build', 'run'))
    depends_on('r-rhdf5lib@1.1.4:', when='@2.14.0:', type=('build', 'run'))

    depends_on('r-ncdf4', when='@2.16.2:', type=('build', 'run'))

    depends_on('gmake', type='build')
