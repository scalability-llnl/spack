# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitFuzzy(PythonPackage):
    """Fuzzy logic toolkit for SciPy"""

    homepage = "https://github.com/scikit-fuzzy/scikit-fuzzy"
    pypi = "scikit-fuzzy/scikit-fuzzy-0.4.2.tar.gz"

    license("BSD-3-Clause")

    version("0.4.2", sha256="1ab12424d847ede1bc79670d8058167be7c8dd660b00756e9b844817ceb1e12e")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build",))
    depends_on("py-networkx@1.9:", type=("build", "run"))
    depends_on("py-numpy@1.6:", type=("build", "run"))
    depends_on("py-scipy@0.9:", type=("build", "run"))
