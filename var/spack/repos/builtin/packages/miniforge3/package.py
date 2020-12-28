# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Miniforge3(Package):
    """Miniforge3 is a minimal installer for conda specific to conda-forge."""

    homepage = "https://github.com/conda-forge/miniforge"
    url      = "https://github.com/conda-forge/miniforge/releases/download/4.8.3-2/Miniforge3-4.8.3-2-Linux-x86_64.sh"

    version('4.8.3-4-Linux-x86_64',
            url='https://github.com/conda-forge/miniforge/releases/download/4.8.3-4/Miniforge3-4.8.3-4-Linux-x86_64.sh',
            sha256='24951262a126582f5f2e1cf82c9cd0fa20e936ef3309fdb8397175f29e647646',
            expand=False)
    version('4.8.3-4-Linux-aarch64',
            url='https://github.com/conda-forge/miniforge/releases/download/4.8.3-4/Miniforge3-4.8.3-4-Linux-aarch64.sh',
            sha256='52a8dde14ecfb633800a2de26543a78315058e30f5883701da1ad2f2d5ba9ed8',
            expand=False)
    version('4.8.3-2-Linux-x86_64',
            url='https://github.com/conda-forge/miniforge/releases/download/4.8.3-2/Miniforge3-4.8.3-2-Linux-x86_64.sh',
            sha256='c8e5b894fe91ce0f86e61065d2247346af107f8d53de0ad89ec848701c4ec1f9',
            expand=False)
    version('4.8.3-2-Linux-aarch64',
            url='https://github.com/conda-forge/miniforge/releases/download/4.8.3-2/Miniforge3-4.8.3-2-Linux-aarch64.sh',
            sha256='bfefc0ede6354568978b4198607edd7f17c2f50ca4c6a47e9f22f8c257c8230a',
            expand=False)
    version('4.8.3-2-MacOSX-x86_64',
            url='https://github.com/conda-forge/miniforge/releases/download/4.8.3-2/Miniforge3-4.8.3-2-MacOSX-x86_64.sh',
            sha256='25ca082ab00a776db356f9bbc660edf6d24659e2aec1cbec5fd4ce992d4d193d',
            expand=False)

    def install(self, spec, prefix):
        mkdirp(prefix)
        pkgname = 'Miniforge3-{0}.sh'.format(self.version)
        chmod = which('chmod')
        chmod('+x', pkgname)
        sh = which('sh')
        sh('./{0}'.format(pkgname), '-b', '-f', '-s', '-p', prefix)
