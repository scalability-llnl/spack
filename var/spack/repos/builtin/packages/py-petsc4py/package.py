# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPetsc4py(PythonPackage):
    """This package provides Python bindings for the PETSc package.
    """

    homepage = "https://gitlab.com/petsc/petsc4py"
    pypi = "petsc4py/petsc4py-3.14.0.tar.gz"
    git      = "https://gitlab.com/petsc/petsc.git"

    maintainers = ['dalcinl', 'balay']

    version('main', branch='main')
    version('3.14.1', sha256='f5f8daf3a4cd1dfc945876b0d83a05b25f3c54e08046312eaa3e3036b24139c0')
    version('3.14.0', sha256='33ac9fb55a541e4c1deabd6e2144da96d5ae70e70c830a55de558000cf3f0ec5')
    version('3.13.0', sha256='0e11679353c0c2938336a3c8d1a439b853e20d3bccd7d614ad1dbea3ec5cb31f')
    version('3.12.0', sha256='4c94a1dbbf244b249436b266ac5fa4e67080d205420805deab5ec162b979df8d')
    version('3.11.0', sha256='ec114b303aadaee032c248a02021e940e43c6437647af0322d95354e6f2c06ad')
    version('3.10.1', sha256='11b59693af0e2067f029924dd6b5220f7a7ec00089f6e2c2361332d6123ea6f7')
    version('3.10.0', sha256='4e58b9e7d4343adcf905751261b789c8c3489496f8de5c3fc3844664ef5ec5a3')
    version('3.9.1',  sha256='8b7f56e0904c57cca08d1c24a1d8151d1554f06c9c5a31b16fb6db3bc928bbd8')
    version('3.9.0',  sha256='ae077dffd455014de16b6ed4ba014ac9e10227dc6b93f919a4229e8e1c870aec')
    version('3.8.1',  sha256='f6260a52dab02247f5b8d686a0587441b1a2048dff52263f1db42e75d2e3f330')
    version('3.8.0',  sha256='3445da12becf23ade4d40cdd04c746581982ab6a27f55fbb5cd29bc5560df4b1')
    version('3.7.0',  sha256='c04931a5ba3fd7c8c8d165aa7908688921ce3cf4cf8725d0cba73380c2107386')

    variant('mpi', default=True,  description='Activates MPI support')

    patch('ldshared.patch', when='@:99')
    patch('ldshared-dev.patch', when='@main')

    depends_on('py-cython', type='build', when='@main')
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))

    depends_on('petsc+mpi', when='+mpi')
    depends_on('petsc~mpi', when='~mpi')
    depends_on('petsc@main', when='@main')
    depends_on('petsc@3.14.2:3.14.99', when='@3.14.1:3.14.99')
    depends_on('petsc@3.14.0:3.14.1', when='@3.14.0')
    depends_on('petsc@3.13:3.13.99', when='@3.13:3.13.99')
    depends_on('petsc@3.12:3.12.99', when='@3.12:3.12.99')
    depends_on('petsc@3.11:3.11.99', when='@3.11:3.11.99')
    depends_on('petsc@3.10.3:3.10.99', when='@3.10.1:3.10.99')
    depends_on('petsc@3.10:3.10.2', when='@3.10.0')
    depends_on('petsc@3.9:3.9.99', when='@3.9:3.9.99')
    depends_on('petsc@3.8:3.8.99', when='@3.8:3.8.99')
    depends_on('petsc@3.7:3.7.99', when='@3.7:3.7.99')
    depends_on('petsc@3.6:3.6.99', when='@3.6:3.6.99')

    @property
    def build_directory(self):
        import os
        if self.spec.satisfies('@main'):
            return os.path.join(self.stage.source_path, 'src', 'binding', 'petsc4py')
        else:
            return self.stage.source_path
