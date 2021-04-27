# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nest(CMakePackage):
    """NEST is a simulator for spiking neural network models

    It focuses on the dynamics, size and structure of neural systems rather
    than on the exact morphology of individual neurons."""

    homepage = "http://www.nest-simulator.org"
    url      = "https://github.com/nest/nest-simulator/releases/download/v2.12.0/nest-2.12.0.tar.gz"
    git      = "https://github.com/nest/nest-simulator.git"

    version('master', branch='master')
    version('2.20.0', sha256='40e33187c22d6e843d80095b221fa7fd5ebe4dbc0116765a91fc5c425dd0eca4')
    version('2.14.0', sha256='d6316d6c9153100a3220488abfa738958c4b65bf2622bd15540e4aa81e79f17f')
    version('2.12.0', sha256='bac578f38bb0621618ee9d5f2f1febfee60cddc000ff32e51a5f5470bb3df40d')
    version('2.10.0', sha256='2b6fc562cd6362e812d94bb742562a5a685fb1c7e08403765dbe123d59b0996c')
    version('2.8.0',  sha256='d47325b27a5599b6ea58a3c4ef06656e7c5a4941c4e94dec6a5c2fa956209915')
    version('2.6.0',  sha256='5fe4924bc57d0c7dd820aa371de935eedf7e813832c0eee2c976b33c9a8db4cf')
    version('2.4.2',  sha256='8f86e58c1a12b733ffabd8b0400326e5a3494a458149ea8ebe9f19674d05b91b')

    variant('python', default=False,
            description='Build the PyNest interface')
    variant('mpi', default=True,
            description='Build with MPI bindings')
    variant('openmp', default=True,
            description='"Enable OpenMP support"')
    variant('optimize', default=True,
            description='Build with MPI bindings')
    variant('modules', default=False,
            description='Enables external module support')
    variant('gsl',     default=True,
            description="Enable GNU Scientific Library")
    variant('shared',   default=True,
            description="Build shared libraries")
    # TODO add variants for neurosim and music when these are in spack

    conflicts('~gsl', when='@:2.10.99',
              msg='Option only introduced for non-ancient versions.')
    conflicts('~shared', when='@:2.10.99',
              msg='Option only introduced for non-ancient versions.')
    conflicts('~openmp', when='@:2.10.99',
              msg='Option only introduced for non-ancient versions.')

    depends_on('python@2.6:',       when='+python', type=('build', 'run'))
    depends_on('py-numpy',          when='+python', type=('build', 'run'))
    depends_on('py-cython@0.19.2:', when='+python', type='build')
    depends_on('py-nose',           when='+python', type='test')
    depends_on('py-setuptools',     when='+python', type='build')

    depends_on('mpi', when='+mpi')

    depends_on('doxygen', type='build')

    depends_on('gsl', when='+gsl')
    depends_on('readline')
    depends_on('libtool')
    depends_on('pkgconfig', type='build')

    extends('python', when='+python')

    # Before 2.12.0 it was an autotools package
    @when('@:2.10.99')
    def cmake(self, spec, prefix):
        pass

    @when('@:2.10.99')
    def build(self, spec, prefix):
        pass

    @when('@:2.10.99')
    def install(self, spec, prefix):
        configure_args = ["CXXFLAGS=-std=c++03",
                          "--prefix=" + prefix,
                          "--with-openmp"]
        if '+python' in spec:
            configure_args.append("--with-python")
        else:
            configure_args.append("--without-python")
        if '+mpi' in spec:
            configure_args.append("--with-mpi")
        else:
            configure_args.append("--without-mpi")
        if '+optimize' in spec:
            configure_args.append("--with-optimize")
        else:
            configure_args.append("--without-optimize")

        configure(*configure_args)

        make()
        make("install")

    def cmake_args(self):
        args = []

        if '+mpi' in self.spec:
            args.append('-Dwith-mpi=ON')
        else:
            args.append('-Dwith-mpi=OFF')

        if '+python' in self.spec:
            version = self.spec['python'].version[0]
            args.append('-Dwith-python={0}'.format(version))
            args.append('-Dcythonize-pynest=' + self.spec['py-cython'].prefix)
        else:
            args.append('-Dwith-python=OFF')
            args.append('-Dcythonize-pynest=OFF')

        if '+optimize' in self.spec:
            args.append('-Dwith-optimize=ON')
        else:
            args.append('-Dwith-optimize=OFF')

        if '+gsl' in self.spec:
            args.append('-Dwith-gsl=' + self.spec['gsl'].prefix)
        else:
            args.append('-Dwith-gsl=OFF')

        if '+openmp' in self.spec:
            args.append('-Dwith-openmp=ON')
        else:
            args.append('-Dwith-openmp=OFF')

        if '+shared' in self.spec:
            args.append('-Dstatic-libraries=OFF')
        else:
            args.append('-Dstatic-libraries=ON')

        return args

    @when('@:2.14.0+modules')
    @run_after('install')
    def install_headers(self):
        # copy source files to installation folder for older versions
        # (these are needed for modules to build against)
        # see https://github.com/nest/nest-simulator/pull/844
        path_headers = join_path(prefix, "include", "nest")

        mkdirp(path_headers)

        for suffix in ["h", "hpp"]:
            for f in find_headers('*.{0}'.format(suffix),
                                  self.stage.source_path, recursive=True):
                install(f, path_headers)

    def setup_run_environment(self, env):
        env.set("NEST_INSTALL_DIR", self.spec.prefix)
