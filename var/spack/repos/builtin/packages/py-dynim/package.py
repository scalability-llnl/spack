# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDynim(PythonPackage):
    """dynim is a pure-python package to perform dynamic-importance
    (DynIm) sampling on a high-dimensional data set."""

    homepage = "https://github.com/LLNL/dynim"
    url = "https://github.com/LLNL/dynim"
    git = "https://github.com/LLNL/dynim.git"

    maintainers("lpottier")

    license("MIT")

    version("main", branch="main", submodules=True)
    version("0.1", commit="aebd780376e7998f7f8b92ba5fdd320bdba7b0d3")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("faiss@1.6.3: +python", type=("build", "run"))
