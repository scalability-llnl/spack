# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pnfft(AutotoolsPackage):
    """PNFFT is a parallel software library for the calculation of
       three-dimensional nonequispaced FFTs."""

    homepage = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software.php.en"
    url = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software/pnfft-1.0.7-alpha.tar.gz"

    version('1.0.7-alpha', sha256='fda558ff57ee3119754363bb6e6739338680d2d6860fe7dc42009d85562bd67a')

    depends_on('pfft')
    depends_on('gsl')

    def configure(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)]
        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")

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
