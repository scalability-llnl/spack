# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUvw(PythonPackage):
    """
    UVW is a small utility library to write VTK files
    from data contained in Numpy arrays.
    """

    homepage = "https://github.com/prs513rosewood/uvw"
    url      = "https://pypi.io/packages/source/u/uvw/uvw-0.3.1.tar.gz"

    maintainers = ['prs513rosewood']

    version('0.3.1', sha256='31e3347ec342bd5381091f3c782ea1a1bfa4709d1de41cd700509e0b813f2265')
    version('0.0.7', sha256='4bcb77cf9655f0dcd5f38f024210ac5ad7ebc6fcfb45f898468d29a927bcb7a5')

    variant('mpi', description="Use parallel writers", default=False)

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'), when="+mpi")
