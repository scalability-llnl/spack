# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install py-torch-scatter
#
# You can edit this file again by typing:
#
#     spack edit py-torch-scatter
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyTorchScatter(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/rusty1s/pytorch_scatter/archive/2.0.5.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('2.0.5', sha256='e29b364beaa9c84a99e0e236be89ed19d4452d89010ff736184ddcce488b47f6')

    depends_on('python@3.6:', type=('build', 'run'))
    extends('py-torch')

    def setup_build_environment(self, env):
        cuda_arches = list(self.spec['py-torch'].variants['cuda_arch'].value)
        for i, x in enumerate(cuda_arches):
            cuda_arches[i] = '{0}.{1}'.format(x[0:-1], x[-1])
        env.set('TORCH_CUDA_ARCH_LIST', str.join(' ', cuda_arches))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
