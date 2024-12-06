# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySparse(PythonPackage):
    """This library provides multi-dimensional sparse arrays."""

    homepage = "https://sparse.pydata.org"
    url = "https://github.com/pydata/sparse/archive/0.11.2.tar.gz"

    license("BSD-3-Clause")

    version("0.11.2", sha256="365b6f038c4d331b3913e5fb00f5bc5dc5eadc49ef2feef332214f9bf33dbc82")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy@0.19:", type=("build", "run"))
    depends_on("py-numba@0.49:", type=("build", "run"))
