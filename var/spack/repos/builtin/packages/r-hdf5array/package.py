# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHdf5array(RPackage):
    """HDF5 backend for DelayedArray objects.

       Implements the HDF5Array and TENxMatrix classes, 2 convenient and
       memory-efficient array-like containers for on-disk representation of
       HDF5 datasets. HDF5Array is for datasets that use the conventional (i.e.
       dense) HDF5 representation. TENxMatrix is for datasets that use the
       HDF5-based sparse matrix representation from 10x Genomics (e.g. the 1.3
       Million Brain Cell Dataset). Both containers being DelayedArray
       extensions, they support all operations supported by DelayedArray
       objects. These operations can be either delayed or block-processed."""

    homepage = "https://bioconductor.org/packages/HDF5Array"
    git      = "https://git.bioconductor.org/packages/HDF5Array.git"

    version('1.12.1', commit='5cfb47664564afcddc6fda221cca0050b283f305')
    version('1.10.1', commit='0b8ae1dfb56e4203dd8e14781850370df46a5e2c')
    version('1.8.1', commit='3c9aa23d117bf489b6341708dc80c943bd1af11a')
    version('1.6.0', commit='95f2f8d3648143abe9dc77c76340c5edf4114c82')
    version('1.4.8', commit='79ab96d123c8da8f8ead81f678fe714c0958ff45')

    depends_on('r@3.6.0:3.6.9', when='@1.12.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.10.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.8.1', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.6.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.4.8', type=('build', 'run'))

    depends_on('r-biocgenerics', when='@1.4.8:', type=('build', 'run'))
    depends_on('r-delayedarray@0.2.4:', when='@1.4.8:', type=('build', 'run'))
    depends_on('r-iranges', when='@1.4.8:', type=('build', 'run'))
    depends_on('r-rhdf5', when='@1.4.8:', type=('build', 'run'))
    depends_on('r-s4vectors', when='@1.4.8:', type=('build', 'run'))

    depends_on('r-delayedarray@0.3.18:', when='@1.6.0:', type=('build', 'run'))

    depends_on('r-biocgenerics@0.25.1:', when='@1.8.1:', type=('build', 'run'))
    depends_on('r-delayedarray@0.5.32:', when='@1.8.1:', type=('build', 'run'))

    depends_on('r-delayedarray@0.7.41:', when='@1.10.1:', type=('build', 'run'))
    depends_on('r-rhdf5@2.25.6:', when='@1.10.1:', type=('build', 'run'))

    depends_on('r-delayedarray@0.9.3:', when='@1.12.1:', type=('build', 'run'))
    depends_on('r-rhdf5lib', when='@1.12.1:', type=('build', 'run'))
    depends_on('r-s4vectors@0.21.6:', when='@1.12.1:', type=('build', 'run'))
