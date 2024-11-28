# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMacs3(PythonPackage):
    """MACS: Model-based Analysis for ChIP-Seq"""

    homepage = "https://github.com/macs3-project/MACS/"
    pypi = "MACS3/MACS3-3.0.0b3.tar.gz"

    maintainers("snehring")

    license("BSD-3-Clause")

    version("3.0.0b3", sha256="caa794d4cfcd7368447eae15878505315dac44c21546e8fecebb3561e9cee362")

    depends_on("c", type="build")  # generated

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("py-setuptools@60.0:", type="build")
    depends_on("py-cython@0.29:0", type=("build", "run"))

    depends_on("py-numpy@1.19:", type=("build", "run"))
    depends_on("py-cykhash@2", type=("build", "run"))
    depends_on("py-hmmlearn@0.3:", type=("build", "run"))

    depends_on("zlib-api")
