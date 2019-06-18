# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nrm(PythonPackage):
    """Node Resource Manager"""

    homepage = "https://xgitlab.cels.anl.gov/argo/nrm"
    url = "https://www.mcs.anl.gov/research/projects/argo/downloads/nrm-0.1.0.tar.gz"
    version('0.1.0', '99a8c8d312fcf3880608cdc8274c285f')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-six', type=('build', 'run'))
    depends_on('py-zmq', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-tornado', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-argparse@1.2.1:', type=('build', 'run'))
    depends_on('py-jsonschema@2.6.0', type=('build', 'run'))
    depends_on('py-warlock', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
