# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Libproxy(CMakePackage):
    """libproxy is a library that provides automatic proxy configuration
    management."""

    homepage = "http://libproxy.github.io/libproxy/"
    url      = "https://github.com/libproxy/libproxy/archive/0.4.15.tar.gz"

    version('0.4.17', sha256='88c624711412665515e2800a7e564aabb5b3ee781b9820eca9168035b0de60a9')
    version('0.4.16', sha256='9e7959d6ae1d6c817f0ac1e253105ce8d99f55d7821c1b6eaef32bf6879c6f0a')
    version('0.4.15', sha256='18f58b0a0043b6881774187427ead158d310127fc46a1c668ad6d207fb28b4e0')
    version('0.4.14', sha256='6220a6cab837a8996116a0568324cadfd09a07ec16b930d2a330e16d5c2e1eb6')
    version('0.4.13', sha256='d610bc0ef81a18ba418d759c5f4f87bf7102229a9153fb397d7d490987330ffd')

    depends_on('zlib')
    depends_on('python', type=('build', 'run'), when='@0.4.16:')
    depends_on('python@:3.6.99', type=('build', 'run'), when='@:0.4.15')
