# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sicer2(PythonPackage):
    """SICER2: a redesigned and improved ChIP-seq broad peak calling tool"""

    homepage = "https://zanglab.github.io/SICER2/"
    pypi = "SICER2/SICER2-1.0.3.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version("1.0.3", sha256="003e0f46fb45717fa6b1c94b2c21416161f5b3a4896fbb335cf2024daf2560dd")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy@1.0.0:", type=("build", "run"))
