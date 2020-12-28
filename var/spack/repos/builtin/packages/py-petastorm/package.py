# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPetastorm(PythonPackage):
    """Petastorm is a library enabling the use of Parquet storage from
    Tensorflow, Pytorch, and other Python-based ML training frameworks."""

    homepage = "https://github.com/uber/petastorm"
    url      = "https://pypi.io/packages/source/p/petastorm/petastorm-0.8.2.tar.gz"

    maintainers = ['adamjstewart']

    version('0.8.2', sha256='7782c315e1ee8d15c7741e3eea41e77b9efce661cf58aa0220a801db64f52f91')

    depends_on('py-setuptools', type='build')
    depends_on('py-dill@0.2.1:', type=('build', 'run'))
    depends_on('py-diskcache@3.0.0:', type=('build', 'run'))
    depends_on('py-future@0.10.2:', type=('build', 'run'))
    depends_on('py-futures@2.0:', type=('build', 'run'), when='^python@:2')
    depends_on('py-numpy@1.13.3:', type=('build', 'run'))
    depends_on('py-packaging@15.0:', type=('build', 'run'))
    depends_on('py-pandas@0.19.0:', type=('build', 'run'))
    depends_on('py-psutil@4.0.0:', type=('build', 'run'))
    depends_on('py-pyspark@2.1.0:', type=('build', 'run'))
    depends_on('py-pyzmq@14.0.0:', type=('build', 'run'))
    depends_on('py-pyarrow@0.12.0:', type=('build', 'run'))
    depends_on('py-six@1.5.0:', type=('build', 'run'))
