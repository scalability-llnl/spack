# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class PyCudf(PythonPackage):
    """Built based on the Apache Arrow columnar memory format,
    cuDF is a GPU DataFrame library for loading, joining,
    aggregating, filtering, and otherwise manipulating data."""

    homepage = "https://rapids.ai"
    url      = "https://github.com/rapidsai/cudf/archive/v0.15.0.tar.gz"

    version('0.15.0',  sha256='2570636b72cce4c52f71e36307f51f630e2f9ea94a1abc018d40ce919ba990e4')

    build_directory = 'python/cudf'

    depends_on('cmake@3.14:', type='build')
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numba@0.40.0:', type=('build', 'run'))
    depends_on('py-numpy@1.14.4:', type=('build', 'run'))
    depends_on('py-pyarrow+cuda+orc+parquet', type=('build', 'run'))
    depends_on('py-pandas@0.23.4:', type=('build', 'run'))
    depends_on('py-rmm', type=('build', 'run'))
    depends_on('cuda@10:')
    depends_on('py-cupy', type=('build', 'run'))
    depends_on('py-fsspec', type=('build', 'run'))

    for v in ('@0.15.0',):
        depends_on('libcudf' + v, when=v)

    phases = ['cmake', 'build_ext', 'install']

    def cmake(self, spec, prefix):
        cmake = which('cmake')

        build_dir = os.path.join(self.stage.source_path, 'cpp', 'build')

        with working_dir(build_dir, create=True):
            cmake('..')
