# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCyvcf2(PythonPackage):
    """fast vcf parsing with cython + htslib"""

    homepage = "https://github.com/brentp/cyvcf2"
    pypi = "cyvcf2/cyvcf2-0.11.7.tar.gz"

    license("MIT")

    version("0.11.7", sha256="a4b6229b89a0a1043684c65cbdd702c366a8800dc3591fb44c4b5a08640cbeec")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-cython@0.23.3:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))

    depends_on("curl")
