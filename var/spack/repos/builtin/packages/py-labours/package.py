# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyLabours(PythonPackage):
    """Python module dependency visualization."""

    homepage = "https://github.com/src-d/hercules"
    url      = "https://github.com/src-d/hercules/archive/v10.7.2.tar.gz"

    version('10.7.2', sha256='4654dcfb1eee5af1610fd05677c6734c2ca1161535fcc14d3933d6debda4bc34')

    build_directory = 'python'

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-matplotlib@2.0:3.999', type=('build', 'run'))
    depends_on('py-numpy@1.12.0:1.999', type=('build', 'run'))
    depends_on('py-pandas@0.20.0:0.999', type=('build', 'run'))
    depends_on('py-pyyaml@3.0:5.999', type=('build', 'run'))
    depends_on('py-scipy@0.19.0:1.2.1', type=('build', 'run'))
    depends_on('py-protobuf@3.5.0:3.999', type=('build', 'run'))
    depends_on('py-munch@2.0:2.999', type=('build', 'run'))
    depends_on('py-python-dateutil@2.6.0:2.999', type=('build', 'run'))
    depends_on('py-tqdm@4.3:4.999', type=('build', 'run'))

    depends_on('py-hdbscan@0.8.0:1.999', type=('build', 'run'))
    depends_on('py-seriate@1.1.2:1.999', type=('build', 'run'))
    depends_on('py-fastdtw@0.3.2:1.999', type=('build', 'run'))
    depends_on('py-lifelines@0.20.0:1.999', type=('build', 'run'))
