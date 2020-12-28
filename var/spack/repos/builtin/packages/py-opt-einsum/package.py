# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOptEinsum(PythonPackage):
    """Optimized Einsum: A tensor contraction order optimizer."""

    homepage = "https://github.com/dgasmith/opt_einsum"
    url      = "https://pypi.io/packages/source/o/opt_einsum/opt_einsum-3.1.0.tar.gz"

    version('3.2.1', sha256='83b76a98d18ae6a5cc7a0d88955a7f74881f0e567a0f4c949d24c942753eb998')
    version('3.2.0', sha256='738b0a1db1d3084d360081bb64d826f9db06d2df7cc0bf8e2c9356028da1fa31')
    version('3.1.0', sha256='edfada4b1d0b3b782ace8bc14e80618ff629abf53143e1e6bbf9bd00b11ece77')
    version('2.3.2', sha256='d3d464b4da7ef09e444c30e4003a27def37f85ff10ff2671e5f7d7813adac35b')

    depends_on('python@:2', type=('build', 'run'), when='@2')
    depends_on('python@3.5:', type=('build', 'run'), when='@3:')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.7:', type=('build', 'run'))
