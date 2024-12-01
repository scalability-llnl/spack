# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHiredis(PythonPackage):
    """Python extension that wraps protocol parsing code in hiredis.
    It primarily speeds up parsing of multi bulk replies."""

    homepage = "https://github.com/redis/hiredis-py"
    pypi = "hiredis/hiredis-1.1.0.tar.gz"

    license("BSD-3-Clause")

    version("1.1.0", sha256="996021ef33e0f50b97ff2d6b5f422a0fe5577de21a8873b58a779a5ddd1c3132")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
