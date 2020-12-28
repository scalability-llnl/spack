# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from glob import glob
from os import unlink

from spack.package import *


class PyDpGpCluster(PythonPackage):
    """DP_GP_cluster clusters genes by expression over a time course using a
       Dirichlet process Gaussian process model."""

    homepage = "https://github.com/PrincetonUniversity/DP_GP_cluster"
    git      = "https://github.com/PrincetonUniversity/DP_GP_cluster.git"

    version('2019-09-22', commit='eec12e74219f916aa86e253783905f7b5e30f6f4')

    depends_on('python@2.7:2.8', type=('build', 'run'))

    depends_on('py-cython', type='build')
    depends_on('py-gpy@0.8.8:0.9.9', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy@0.14:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))

    @run_before('build')
    def remove_cython_output(self):
        for f in glob('DP_GP/*.c'):
            unlink(f)
