# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMacholib(PythonPackage):
    """Python package for Mach-O header analysis and editing"""

    pypi = "macholib/macholib-1.11.tar.gz"

    license("MIT")

    version("1.16", sha256="001bf281279b986a66d7821790d734e61150d52f40c080899df8fefae056e9f7")
    version("1.11", sha256="c4180ffc6f909bf8db6cd81cff4b6f601d575568f4d5dee148c830e9851eb9db")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-altgraph@0.15:", type=("build", "run"))
