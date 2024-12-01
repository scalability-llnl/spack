# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygdbmi(PythonPackage):
    """Parse gdb machine interface output with Python"""

    homepage = "https://github.com/cs01/pygdbmi"
    pypi = "pygdbmi/pygdbmi-0.8.2.0.tar.gz"

    license("MIT")

    version("0.9.0.3", sha256="5bdf2f072e8f2f6471f19f8dcd87d6425c5d8069d47c0a5ffe8d0eff48cb171e")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
