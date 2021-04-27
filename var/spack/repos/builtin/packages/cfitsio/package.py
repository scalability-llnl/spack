# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Cfitsio(AutotoolsPackage):
    """CFITSIO is a library of C and Fortran subroutines for reading and writing
    data files in FITS (Flexible Image Transport System) data format.
    """

    homepage = 'http://heasarc.gsfc.nasa.gov/fitsio/'
    url      = 'http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.49.tar.gz'

    version('3.49', sha256='5b65a20d5c53494ec8f638267fca4a629836b7ac8dd0ef0266834eab270ed4b3')
    version('3.48', sha256='91b48ffef544eb8ea3908543052331072c99bf09ceb139cb3c6977fc3e47aac1')
    version('3.47', sha256='418516f10ee1e0f1b520926eeca6b77ce639bed88804c7c545e74f26b3edf4ef')
    version('3.45', sha256='bf6012dbe668ecb22c399c4b7b2814557ee282c74a7d5dc704eb17c30d9fb92e')
    version('3.42', sha256='6c10aa636118fa12d9a5e2e66f22c6436fb358da2af6dbf7e133c142e2ac16b8')
    version('3.41', sha256='a556ac7ea1965545dcb4d41cfef8e4915eeb8c0faa1b52f7ff70870f8bb5734c')
    version('3.37', sha256='092897c6dae4dfe42d91d35a738e45e8236aa3d8f9b3ffc7f0e6545b8319c63a')

    variant('bzip2', default=True, description='Enable bzip2 support')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('curl')
    depends_on('bzip2', when='+bzip2')

    def url_for_version(self, version):
        if version >= Version('3.47'):
            return super(Cfitsio, self).url_for_version(version)

        url = 'http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio{0}0.tar.gz'
        return url.format(version.joined)

    def configure_args(self):
        spec = self.spec
        extra_args = []
        if '+bzip2' in spec:
            extra_args.append('--with-bzip2=%s' % spec['bzip2'].prefix),
        return extra_args

    @property
    def build_targets(self):
        targets = ['all']

        # Build shared if variant is set.
        if '+shared' in self.spec:
            targets += ['shared']

        return targets
