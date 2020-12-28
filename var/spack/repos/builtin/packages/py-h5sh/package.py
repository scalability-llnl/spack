# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH5sh(PythonPackage):
    """Shell-like environment for HDF5."""

    homepage = "https://pypi.python.org/pypi/h5sh"
    url      = "https://github.com/sethrj/h5sh/archive/v0.1.1.tar.gz"

    maintainers = ['sethrj']

    version('0.1.1', sha256='111989d8200d1da8e150aee637a907e524ca0f98d5005a55587cba0d94d9c4a0')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-prompt-toolkit@2:', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
