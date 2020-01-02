# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCrossmap(PythonPackage):
    """CrossMap is a program for convenient conversion of genome coordinates
       (or annotation files) between different assemblies"""

    homepage = "http://crossmap.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/crossmap/CrossMap-0.3.3.tar.gz"

    version('0.3.3', sha256='56d99fd606e13e399b83438953d0d89fc281df1c1e8e47eed7d773e7ec9c88f8')
    version('0.2.9', sha256='57243ee5051352c93088874c797ceac0426f249704ba897360fb628b3365d0af')

    depends_on('python@3:', type=('build', 'run'), when='@0.3.0:')
    depends_on('python@2.7:2.8', type=('build', 'run'), when='@:0.2.9')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-bx-python', type=('build', 'run'))

    depends_on('py-pybigwig', type=('build', 'run'), when='@0.3.0:')
