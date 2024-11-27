# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLoompy(PythonPackage):
    """Work with Loom files for single-cell RNA-seq data."""

    homepage = "https://github.com/linnarsson-lab/loompy"
    pypi = "loompy/loompy-3.0.7.tar.gz"

    license("BSD-2-Clause")

    version("3.0.7", sha256="b5cdf7b54734c6bed3a181d11947af70af2c6e0dcadc02fd0e871df232faa8f4")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-numpy-groupies", type=("build", "run"))
