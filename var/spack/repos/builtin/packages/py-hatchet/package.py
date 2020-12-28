# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchet(PythonPackage):
    """Hatchet is an analysis tool for structured tree or graph performance data
    using an indexed Pandas dataframe."""

    homepage = "https://github.com/LLNL/hatchet"
    url      = "https://github.com/LLNL/hatchet/archive/v1.0.0.tar.gz"

    maintainers = ["slabasan", "bhatele", "tgamblin"]

    version('1.0.0', sha256='efd218bc9152abde0a8006489a2c432742f00283a114c1eeb6d25abc10f5862d')

    depends_on('python@2.7,3:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-pandas',     type=('build', 'run'))
    depends_on('py-pydot',      type=('build', 'run'))
    depends_on('py-pyyaml',     type=('build', 'run'))
