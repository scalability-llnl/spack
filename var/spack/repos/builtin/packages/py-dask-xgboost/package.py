# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDaskXgboost(PythonPackage):
    """Distributed training with XGBoost and Dask.distributed.

    Deprecated: use `py-xgboost+dask` instead."""

    homepage = "https://github.com/dask/dask-xgboost/"
    pypi = "dask-xgboost/dask-xgboost-0.1.11.tar.gz"

    # Deprecated, see https://github.com/dask/dask-xgboost/issues/80
    version('0.1.11', sha256='3fbe1bf4344dc74edfbe9f928c7e3e6acc26dc57cefd8da8ae56a15469c6941c', deprecated=True)

    variant('sparse', default=False, description='Add sparse support')

    depends_on('py-setuptools', type='build')
    depends_on('py-xgboost@:0.90', type=('build', 'run'))
    depends_on('py-dask', type=('build', 'run'))
    depends_on('py-distributed@1.15.2:', type=('build', 'run'))

    depends_on('py-sparse', type=('build', 'run'), when='+sparse')
    depends_on('py-scipy', type=('build', 'run'), when='+sparse')
