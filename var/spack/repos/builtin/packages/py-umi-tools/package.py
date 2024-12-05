# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUmiTools(PythonPackage):
    """Tools for handling Unique Molecular Identifiers in NGS data sets"""

    homepage = "https://github.com/CGATOxford/UMI-tools"
    url = "https://github.com/CGATOxford/UMI-tools/archive/0.5.3.tar.gz"

    license("MIT")

    version("1.1.4", sha256="945c4c98e2007369c301a7a009c6f9deb0fda74b0117cd14e14bd134164a4ff6")
    version("1.0.0", sha256="7f73ef29120134123351c19089e9b7b7c03a8f241a19f8cb0e43d17f0e2f9fc7")
    version("0.5.5", sha256="9834a4388dd1ea0b971071009db7ccdbd447c6019796a3c061b0bb383c9ad992")
    version("0.5.4", sha256="a03e6babf188d0618a63f083b4da18120b9e8b4d473af71b585dba7de347e962")
    version("0.5.3", sha256="d599f15c48c96a96ba667db1f364ebfed4ba733dd30469f9656c1717282d2ecb")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@1.1:", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-pandas@0.12:", type=("build", "run"))
    depends_on("py-pysam@0.8.4:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pybktree", type=("build", "run"), when="@1.1.0:")
