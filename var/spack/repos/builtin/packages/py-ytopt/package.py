# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYtopt(PythonPackage):
    """Ytopt package implements search using Random Forest (SuRF), an autotuning
       search method developed within Y-Tune ECP project."""

    homepage = "https://xgitlab.cels.anl.gov/pbalapra/ytopt"
    url      = "https://xgitlab.cels.anl.gov/pbalapra/ytopt/raw/release/dist/ytopt-0.1.0.tar.gz"

    version('0.1.0', sha256='c7081fe3585a5b7a25bcb84733cd2326b72de3bfc4f84d6ad110341f24c3e612')

    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('py-scikit-optimize', type=('build', 'run'))

    def build_args(self, spec, prefix):
        args = []
        return args
