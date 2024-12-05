# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorio(PythonPackage):
    """Tools for color research"""

    homepage = "https://github.com/nschloe/colorio"
    pypi = "colorio/colorio-0.11.2.tar.gz"

    license("GPL-3.0-or-later")

    version("0.11.2", sha256="aa45d8e0a2e506c4019d4fb488d34a107d7f803c8e8ff355e2e57c01f6f1cd81")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-core@3.2:3.6", type="build")
    depends_on("py-numpy@1.20:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-npx", type=("build", "run"))
