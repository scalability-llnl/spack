# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYaspin(PythonPackage):
    """Yet Another Terminal Spinner"""

    homepage = "https://github.com/pavdmyt/yaspin"
    pypi = "yaspin/yaspin-2.1.0.tar.gz"

    license("MIT")

    version("2.1.0", sha256="c8d34eca9fda3f4dfbe59f57f3cf0f3641af3eefbf1544fbeb9b3bacf82c580a")

    depends_on("python@3.6.2:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-termcolor@1.1.0:1", type=("build", "run"))
