# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGluoncv(PythonPackage):
    """GluonCV provides implementations of state-of-the-art
    (SOTA) deep learning algorithms in computer vision. It aims
    to help engineers, researchers, and students quickly
    prototype products, validate new ideas and learn computer
    vision."""

    homepage = "https://gluon-cv.mxnet.io/"
    url      = "https://github.com/dmlc/gluon-cv/archive/v0.6.0.tar.gz"

    version('0.6.0', sha256='5ac89d73f34d02b2e60595a5cc35f46d0a69376567fae3a9518005dd89161305')

    depends_on('py-setuptools',  type='build')
    depends_on('py-numpy',       type=('build', 'run'))
    depends_on('py-tqdm',        type=('build', 'run'))
    depends_on('py-requests',    type=('build', 'run'))
    depends_on('py-matplotlib',  type=('build', 'run'))
    depends_on('py-portalocker', type=('build', 'run'))
    depends_on('pil',            type=('build', 'run'))
    depends_on('py-scipy',       type=('build', 'run'))
    depends_on('py-cython',      type='build')

    patch('no-unicode-readme.patch')

    def build_args(self, spec, prefix):
        args = []
        args.append('--with-cython')
        return args
