# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDnaio(PythonPackage):
    """Read and write FASTQ and FASTA"""

    homepage = "https://github.com/marcelm/dnaio"
    url      = "https://pypi.io/packages/source/d/dnaio/dnaio-0.3.tar.gz"
    git      = "https://github.com/marcelm/dnaio.git"

    version('0.4.2', sha256='fa55a45bfd5d9272409b714158fb3a7de5dceac1034a0af84502c7f503ee84f8')
    version('0.3', sha256='47e4449affad0981978fe986684fc0d9c39736f05a157f6cf80e54dae0a92638')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', when='@0.4:', type='build')
    depends_on('py-xopen', type=('build', 'run'))
    depends_on('py-xopen@0.8.2:', when='@0.4:', type=('build', 'run'))
