# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-lightgbm
#
# You can edit this file again by typing:
#
#     spack edit py-lightgbm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyLightgbm(PythonPackage):
    """LightGBM is a gradient boosting framework that uses tree
    based learning algorithms."""

    homepage = "https://github.com/microsoft/LightGBM"
    pypi     = "lightgbm/lightgbm-3.1.1.tar.gz"

    version('3.1.1', sha256='babece2e3613e97748a67ed45387bb0e984bdb1f4126e39f010fbfe7503c7b20')

    variant('mpi', default=False, description="Build with mpi support")

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scikit-learn@:0.21.999,0.22.1:', type=('build', 'run'))

    depends_on('cmake@3.8:', type='build')

    depends_on('mpi', when='+mpi')

    def install_args(self, spec, prefix):
        args = []

        if spec.satisfies('+mpi'):
            args.append('--mpi')

        return args
