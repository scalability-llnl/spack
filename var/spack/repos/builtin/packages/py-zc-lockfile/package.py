# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZcLockfile(PythonPackage):
    """Basic inter-process locks"""

    pypi = "zc.lockfile/zc.lockfile-1.4.tar.gz"

    license("ZPL-2.1")

    version("1.4", sha256="95a8e3846937ab2991b61703d6e0251d5abb9604e18412e2714e1b90db173253")

    depends_on("py-setuptools", type=("build", "run"))
