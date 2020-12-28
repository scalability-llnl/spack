# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCutadapt(PythonPackage):
    """Cutadapt finds and removes adapter sequences, primers, poly-A tails and
    other types of unwanted sequence from your high-throughput sequencing
    reads."""

    homepage = "https://cutadapt.readthedocs.io"
    url      = "https://pypi.io/packages/source/c/cutadapt/cutadapt-1.13.tar.gz"
    git      = "https://github.com/marcelm/cutadapt.git"

    version('2.10', sha256='936b88374b5b393a954852a0fe317a85b798dd4faf5ec52cf3ef4f3c062c242a')
    version('2.9', sha256='cad8875b461ca09cea498b4f0e78b0d3dcd7ea84d27d51dac4ed45080bf1499e')
    version('2.5', sha256='ced79e49b93e922e579d0bb9d21298dcb2d7b7b1ea721feed484277e08b1660b')
    version('1.13', sha256='aa9f2c1f33dc081fe94f42b1250e4382b8fb42cabbf6e70a76ff079f211d5fc0')

    depends_on('python@2.6:', type=('build', 'run'), when='@1.13')
    depends_on('python@3.4:', type=('build', 'run'), when='@2.0:2.5')
    depends_on('python@3.5:', type=('build', 'run'), when='@2.6:')
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build', when='@2.0:')
    depends_on('py-xopen@0.1.1:', type=('build', 'run'), when='@1.13')
    depends_on('py-xopen@0.5.0:', type=('build', 'run'), when='@2.0:2.3')
    depends_on('py-xopen@0.7.3:', type=('build', 'run'), when='@2.4')
    depends_on('py-xopen@0.8.1:0.8.999', type=('build', 'run'), when='@2.5')
    depends_on('py-xopen@0.8.4:0.8.999', type=('build', 'run'), when='@2.6:')
    depends_on('py-dnaio@0.3:', type=('build', 'run'), when='@2.0:2.4')
    depends_on('py-dnaio@0.3.0:0.3.999', type=('build', 'run'), when='@2.5')
    depends_on('py-dnaio@0.4.0:0.4.999', type=('build', 'run'), when='@2.6')
    depends_on('py-dnaio@0.4.1:0.4.999', type=('build', 'run'), when='@2.7:2.9')
    depends_on('py-dnaio@0.4.2:0.4.999', type=('build', 'run'), when='@2.10:')
