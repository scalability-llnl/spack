# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Simulationio(CMakePackage):
    """SimulationIO: Efficient and convenient I/O for large PDE simulations"""

    homepage = "https://github.com/eschnett/SimulationIO"
    url      = "https://github.com/eschnett/SimulationIO/archive/version/9.0.1.tar.gz"
    git      = "https://github.com/eschnett/SimulationIO.git"

    maintainers = ['eschnett']

    version('master', branch='master')
    version('9.0.1', sha256='c2f6c99417165f6eb8cbb9c44822d119586675abb34eabd553eb80f44b53e0c8')

    variant('julia', default=False, description="Enable Julia bindings")
    variant('python', default=True, description="Enable Python bindings")

    variant('pic', default=True,
            description="Produce position-independent code")

    depends_on("asdf-cxx ~python", when='~python')
    depends_on("asdf-cxx +python", when='+python')
    depends_on('hdf5 +cxx @1.10.1:')
    depends_on('julia', when='+julia', type=('build', 'run'))
    depends_on('py-h5py', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('python@3:', when='@9: +python', type=('build', 'run'))
    depends_on('python@2.7:2.8', when='@:8 +python', type=('build', 'run'))
    depends_on('swig', type='build')

    extends('python')

    def cmake_args(self):
        spec = self.spec
        options = []
        if '+pic' in spec:
            options.append("-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true")
        return options

    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAILURE=1")
