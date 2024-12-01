# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPkgutilResolveName(PythonPackage):
    """Resolve a name to an object. A backport of Python 3.9 `pkgutil.resolve_name`"""

    homepage = "https://github.com/graingert/pkgutil-resolve-name"
    pypi = "pkgutil_resolve_name/pkgutil_resolve_name-1.3.10.tar.gz"

    version("1.3.10", sha256="357d6c9e6a755653cfd78893817c0853af365dd51ec97f3d358a819373bbd174")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-flit-core@2", type="build")
