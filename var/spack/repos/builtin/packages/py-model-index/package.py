# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModelIndex(PythonPackage):
    """Create a source of truth for ML model results and browse it on Papers with Code"""

    homepage = "https://github.com/paperswithcode/model-index"
    git = "https://github.com/paperswithcode/model-index.git"

    license("MIT")

    version("0.1.11", commit="a39af5f8aaa2a90b8fc7180744a855282360067a")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-markdown", type=("build", "run"))
    depends_on("py-ordered-set", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
