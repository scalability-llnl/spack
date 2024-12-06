# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytaridx(PythonPackage):
    """Python module/library for creating and maintaining a rapidly searchable
    index for a tar-file. This allows "direct access" of members (files) in
    the tar archive."""

    homepage = "https://github.com/LLNL/pytaridx"
    git = "https://github.com/LLNL/pytaridx.git"
    pypi = "pytaridx/pytaridx-1.0.2.tar.gz"

    maintainers("bhatiaharsh")

    license("MIT")

    version("1.0.2", sha256="702c42ade13ae8688a56a8edfcd7e0e7512a489a22796c6cfdbcef677010ee47")
    version("master", branch="master")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
