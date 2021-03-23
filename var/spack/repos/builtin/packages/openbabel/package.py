# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Openbabel(CMakePackage):
    """Open Babel is a chemical toolbox designed to speak the many languages
    of chemical data. It's an open, collaborative project allowing anyone to
    search, convert, analyze, or store data from molecular modeling, chemistry,
    solid-state materials, biochemistry, or related areas."""

    homepage = 'https://openbabel.org/wiki/Main_Page'
    url = 'https://github.com/openbabel/openbabel/archive/openbabel-3-0-0.tar.gz'
    git = 'https://github.com/openbabel/openbabel.git'

    version('master', branch='master')
    version('3.0.0', tag='openbabel-3-0-0')
    version('2.4.1', tag='openbabel-2-4-1')
    version('2.4.0', tag='openbabel-2-4-0')

    variant('python', default=True, description='Build Python bindings')

    extends('python', when='+python')

    depends_on('python', type=('build', 'run'), when='+python')
    depends_on('cmake@3.1:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('swig@2.0:', type='build', when='+python')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('cairo')       # required to support PNG depiction
    depends_on('pango')       # custom cairo requires custom pango
    depends_on('eigen@3.0:')  # required if using the language bindings
    depends_on('libxml2')     # required to read/write CML files, XML formats
    depends_on('zlib')        # required to support reading gzipped files
    depends_on('rapidjson')   # required to support JSON
    depends_on('libsm')
    depends_on('uuid')

    # Needed for Python 3.6 support
    patch('python-3.6-rtld-global.patch', when='@:2.4.1+python')

    # Convert tabs to spaces. Allows unit tests to pass
    patch('testpdbformat-tabs-to-spaces.patch', when='@:2.4.1')

    def cmake_args(self):
        spec = self.spec
        args = []

        if '+python' in spec:
            args.extend([
                '-DPYTHON_BINDINGS=ON',
                '-DPYTHON_EXECUTABLE={0}'.format(spec['python'].command.path),
                '-DRUN_SWIG=ON',
            ])
        else:
            args.append('-DPYTHON_BINDINGS=OFF')

        args.append('-DWITH_MAEPARSER=OFF')  # maeparser is currently broken

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        obabel = Executable(join_path(self.prefix.bin, 'obabel'))
        obabel('-:C1=CC=CC=C1Br', '-omol')

        if '+python' in self.spec:
            python('-c', 'import openbabel')
            if self.spec.version < Version('3.0.0'):
                python('-c', 'import pybel')
