# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymol(PythonPackage):
    """PyMOL is a Python-enhanced molecular graphics tool. It excels at 3D
       visualization of proteins, small molecules, density, surfaces, and
       trajectories. It also includes molecular editing, ray tracing, and
       movies. Open Source PyMOL is free to everyone!"""

    homepage = "https://pymol.org"
    url      = "https://github.com/schrodinger/pymol-open-source/archive/v2.4.0.tar.gz"

    version('2.4.0', sha256='5ede4ce2e8f53713c5ee64f5905b2d29bf01e4391da7e536ce8909d6b9116581')
    version('2.3.0', sha256='62aa21fafd1db805c876f89466e47513809f8198395e1f00a5f5cc40d6f40ed0')

    depends_on('python+tkinter', type=('build', 'run'))
    depends_on('freetype', type=('build', 'run'))
    depends_on('glew', type=('build'))
    depends_on('glm', type=('build'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('tcsh', type=('build', 'run'))
    depends_on('py-pyqt5', type=('build', 'run'))
    depends_on('py-pmw', type=('build', 'run'))
    depends_on('libmmtf-cpp', type=('build', 'run', 'link'))
    depends_on('msgpack-c', type=('build', 'run'))
    depends_on('libpng@1.5.13', type=('build', 'run'))

    def setup_build_environment(self, env):
        include = []
        library = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            include.extend(query.headers.directories)

        env.set('CPATH', ':'.join(include))
        env.set('LIBRARY_PATH', ':'.join(library))
        env.set('PREFIX_PATH', self.spec['libpng'].prefix)
        env.prepend_path('PREFIX_PATH', self.spec['py-pyqt5'].prefix)
