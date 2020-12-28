# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Muparser(Package):
    """C++ math expression parser library."""
    homepage = "http://muparser.beltoforion.de/"
    url      = "https://github.com/beltoforion/muparser/archive/v2.2.5.tar.gz"

    version('2.2.6.1', sha256='d2562853d972b6ddb07af47ce8a1cdeeb8bb3fa9e8da308746de391db67897b3')
    version('2.2.5', sha256='0666ef55da72c3e356ca85b6a0084d56b05dd740c3c21d26d372085aa2c6e708')

    # Replace std::auto_ptr by std::unique_ptr
    # https://github.com/beltoforion/muparser/pull/46
    patch('auto_ptr.patch',
          when='@2.2.5')

    depends_on('cmake@3.1.0:', when='@2.2.6:', type='build')

    # Cmake build since 2.2.6
    @when('@2.2.6:')
    def install(self, spec, prefix):
        cmake_args = [
            '-DENABLE_SAMPLES=OFF',
            '-DENABLE_OPENMP=OFF',
            '-DBUILD_SHARED_LIBS=ON'
        ]

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')

    @when('@2.2.5')
    def install(self, spec, prefix):
        options = ['--disable-debug',
                   '--disable-samples',
                   '--disable-dependency-tracking',
                   'CXXFLAGS={0}'.format(self.compiler.cxx11_flag),
                   '--prefix=%s' % prefix]

        configure(*options)

        make(parallel=False)
        make("install")
