# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBeachmat(RPackage):
    """Compiling Bioconductor to Handle Each Matrix Type.

       Provides a consistent C++ class interface for reading from and writing
       data to a variety of commonly used matrix types. Ordinary matrices and
       several sparse/dense Matrix classes are directly supported, third-party
       S4 classes may be supported by external linkage, while all other
       matrices are handled by DelayedArray block processing."""

    homepage = "https://bioconductor.org/packages/beachmat"
    git      = "https://git.bioconductor.org/packages/beachmat.git"

    version('2.0.0', commit='2bdac6ce7b636fd16f78641a0bcc2181670107ab')
    version('1.4.0', commit='e3b7a21cae0080d077a0d40e35d1d148f088720a')
    version('1.2.1', commit='ebae81772045a314e568c2f7d73ea3b27e7bf7d8')
    version('1.0.2', commit='6bd57b91d6428ac916f46572d685d3cb01a757f7')

    depends_on('r@3.4:', type=('build', 'run'))
    depends_on('r-rhdf5lib', when='@1.0.2:1.4.0', type=('build', 'run'))
    depends_on('r-hdf5array', when='@1.0.2:1.4.0', type=('build', 'run'))
    depends_on('r-delayedarray', type=('build', 'run'))
    depends_on('r-rcpp@0.12.14:', when='@1.0.2:1.4.0', type=('build', 'run'))
    depends_on('r-rhdf5', when='@1.0.2:1.4.0', type=('build', 'run'))

    depends_on('r@3.5:', when='@1.2.1:1.4.0', type=('build', 'run'))
    depends_on('r-rhdf5lib@1.1.4:', when='@1.2.1', type=('build', 'run'))
    depends_on('r-hdf5array@1.7.3:', when='@1.2.1', type=('build', 'run'))
    depends_on('r-delayedarray@0.5.30:', when='@1.2.1', type=('build', 'run'))

    depends_on('r-hdf5array@1.9.5:', when='@1.4.0', type=('build', 'run'))
    depends_on('r-delayedarray@0.7.38:', when='@1.4.0', type=('build', 'run'))
    depends_on('r-biocgenerics', when='@1.4.0:', type=('build', 'run'))
