# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitSparse(PythonPackage):
    """Sparse matrix tools extending scipy.sparse, but with incompatible licenses"""

    homepage = "https://github.com/scikit-sparse/scikit-sparse"
    pypi = "scikit-sparse/scikit-sparse-0.4.8.tar.gz"
    git = "https://github.com/scikit-sparse/scikit-sparse.git"

    maintainers("cgcgcg")

    license("BSD-2-Clause")

    version("0.4.12", sha256="e6502fea9ba561cfa5491eb222ed2c81c16263d8182a293950db20509c941166")
    version("0.4.11", sha256="64c61a8777b7c7ba8e1f2bf76bc767f740e6426f1cce2d90f1324b177618e1ca")
    version("0.4.8", sha256="2a224c60da3ef951975242ea777478583d3265efc72db5cfb7861686521a4009")

    depends_on("python@3.6:3.11", when="@0.4.12", type=("build", "link", "run"))
    depends_on("python@3.6:3.11", when="@0.4.11", type=("build", "link", "run"))
    depends_on("python@3.6:3.10", when="@0.4.8", type=("build", "link", "run"))
    depends_on("py-setuptools@40.8:", type="build")
    depends_on("py-cython@0.22:", when="@0.4.12", type="build")
    depends_on("py-cython@0.22:0.29", when="@:0.4.11", type="build")
    depends_on("py-numpy@1.13.3:", type=("build", "link", "run"))
    # https://github.com/scikit-sparse/scikit-sparse/issues/120
    depends_on("py-numpy@:1", type=("build", "link", "run"))
    depends_on("py-scipy@0.19:", type="run")
    depends_on("suite-sparse", type=("build", "link", "run"))

    import_modules = ["sksparse"]
