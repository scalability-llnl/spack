# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPtyprocess(PythonPackage):
    """Run a subprocess in a pseudo terminal"""

    homepage = "https://pypi.python.org/pypi/ptyprocess"
    url      = "https://pypi.io/packages/source/p/ptyprocess/ptyprocess-0.5.1.tar.gz"

    version('0.6.0', sha256='923f299cc5ad920c68f2bc0bc98b75b9f838b93b599941a6b63ddbc2476394c0')
    version('0.5.1', sha256='0530ce63a9295bfae7bd06edc02b6aa935619f486f0f1dc0972f516265ee81a6')
