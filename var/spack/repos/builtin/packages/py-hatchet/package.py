# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyHatchet(PythonPackage):
    """Hatchet is a performance tool for analyzing hierarchical performance data
    using a graph-indexed Pandas dataframe."""

    homepage = "https://github.com/hatchet/hatchet"
    url      = "https://github.com/hatchet/hatchet/archive/v1.0.0.tar.gz"

    maintainers = ["slabasan", "bhatele", "tgamblin"]

    version('1.3.0', sha256='d38212aec6272558e25538ff23b54ec0f2b4dbf6ef4b0e77f7f05c37c0d17815')
    version('1.2.0', sha256='1d5f80abfa69d1a379dff7263908c5c915023f18f26d50b639556e2f43ac755e')
    version('1.1.0', sha256='71bfa2881ef295294e5b4493acb8cce98d14c354e9ae59b42fb56a76d8ec7056')
    version('1.0.1', sha256='e5a4b455ab6bfbccbce3260673d9af8d1e4b21e19a2b6d0b6c1e1d7727613b7a')
    version('1.0.0', sha256='efd218bc9152abde0a8006489a2c432742f00283a114c1eeb6d25abc10f5862d')

    depends_on('python@2.7,3:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-pandas',     type=('build', 'run'))
    depends_on('py-pydot',      type=('build', 'run'))
    depends_on('py-pyyaml',     type=('build', 'run'))
