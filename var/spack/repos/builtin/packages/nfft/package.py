# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nfft(AutotoolsPackage):
    """NFFT is a C subroutine library for computing the nonequispaced discrete
    Fourier transform (NDFT) in one or more dimensions, of arbitrary input
    size, and of complex data."""

    homepage = "https://www-user.tu-chemnitz.de/~potts/nfft"
    url = "https://github.com/NFFT/nfft/releases/download/3.4.1/nfft-3.4.1.tar.gz"

    version('3.4.1', sha256='1cf6060eec0afabbbba323929d8222397a77fa8661ca74927932499db26b4aaf')
    version('3.3.2', sha256='9dcebd905a82c4f0a339d0d5e666b68c507169d9173b66d5ac588aae5d50b57c')

    depends_on('fftw')

    def configure(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)]

        configure = Executable('../configure')

        if '+double' in spec['fftw']:
            with working_dir('double', create=True):
                configure(*options)
        if '+float' in spec['fftw']:
            with working_dir('float', create=True):
                configure('--enable-float', *options)
        if '+long_double' in spec['fftw']:
            with working_dir('long-double', create=True):
                configure('--enable-long-double', *options)

    def build(self, spec, prefix):
        if '+double' in spec['fftw']:
            with working_dir('double'):
                make()
        if '+float' in spec['fftw']:
            with working_dir('float'):
                make()
        if '+long_double' in spec['fftw']:
            with working_dir('long-double'):
                make()

    def check(self):
        spec = self.spec
        if '+double' in spec['fftw']:
            with working_dir('double'):
                make("check")
        if '+float' in spec['fftw']:
            with working_dir('float'):
                make("check")
        if '+long_double' in spec['fftw']:
            with working_dir('long-double'):
                make("check")

    def install(self, spec, prefix):
        if '+double' in spec['fftw']:
            with working_dir('double'):
                make("install")
        if '+float' in spec['fftw']:
            with working_dir('float'):
                make("install")
        if '+long_double' in spec['fftw']:
            with working_dir('long-double'):
                make("install")
