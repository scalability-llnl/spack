# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyBashKernel(PythonPackage):
    """A Jupyter kernel for bash."""

    homepage = "https://github.com/takluyver/bash_kernel"
    pypi     = "bash_kernel/bash_kernel-0.7.2.tar.gz"

    version('0.7.2', sha256='a08c84eddd8179de5234105821fd5cc210015671a0bd3cd0bc4f631c475e1670')

    depends_on('py-pexpect@4.0:', type=('build', 'run'))
