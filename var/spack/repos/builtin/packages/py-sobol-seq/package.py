# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySobolSeq(PythonPackage):
    """Sobol sequence implementation in python"""

    homepage = "https://github.com/naught101/sobol_seq"
    pypi = "sobol_seq/sobol_seq-0.2.0.tar.gz"

    license("MIT")

    version("0.2.0", sha256="e16e701bd7b03ec6ce65b3a64c9205799f6a2d00c2054dd8c4ff4343f3981172")

    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
