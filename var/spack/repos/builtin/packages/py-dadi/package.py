# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDadi(PythonPackage):
    """Fit population genetic models of demography and selection using
    diffusion approximations to the allele frequency spectrum """

    homepage = "https://bitbucket.org/gutenkunstlab/dadi/src/master/"
    git      = "https://bitbucket.org/gutenkunstlab/dadi.git"
    url      = "https://files.pythonhosted.org/packages/ef/2d/b8636392a28b5d7fe2665a15ab9899651ed7e2af7264c8685e648371aa5c/dadi-2.1.0.tar.gz"

    maintainers = ['dorton21']

    version('2020-12-02', commit='047bac0')
    version('2.1.0', sha256='97a15aa7ef501850cad4cff66b11b66ecb65d5d68acbf2ff713585c81c3a1038')

    depends_on('py-setuptools', type=('build'))
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('nlopt', type=('build', 'run'))
