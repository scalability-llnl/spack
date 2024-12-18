# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchCython(PythonPackage):
    """cython hooks for hatch"""

    homepage = "https://github.com/joshua-auchincloss/hatch-cython"
    pypi = "hatch_cython/hatch_cython-0.5.1.tar.gz"

    license("MIT")

    version("0.5.1", sha256="d01135e092544069c3e61f6dc36748ee369beacb893a5c43b9593a533f839703")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-hatchling", type=("build", "run"))
    depends_on("py-hatch", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
    depends_on("py-typing-extensions", when="@:3.9", type=("build", "run"))
