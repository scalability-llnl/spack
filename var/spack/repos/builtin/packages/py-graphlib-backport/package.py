# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGraphlibBackport(PythonPackage):
    """Backport of the Python 3.9 graphlib module for Python 3.6+."""

    homepage = "https://github.com/mariushelf/graphlib_backport"
    pypi = "graphlib_backport/graphlib_backport-1.0.3.tar.gz"

    version("1.0.3", sha256="7bb8fc7757b8ae4e6d8000a26cd49e9232aaa9a3aa57edb478474b8424bfaae2")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-poetry@1:", type="build")
