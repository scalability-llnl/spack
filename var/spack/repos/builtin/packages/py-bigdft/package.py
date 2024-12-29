# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBigdft(PythonPackage):
    """BigDFT: the python interface of BigDFT for electronic structure calculation
    based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.5", sha256="5fe51e92bb746569207295feebbcd154ce4f1b364a3981bace75c45e983b2741")
    version("1.9.4", sha256="fa22115e6353e553d2277bf054eb73a4710e92dfeb1ed9c5bf245337187f393d")
    version("1.9.3", sha256="f5f3da95d7552219f94366b4d2a524b2beac988fb2921673a65a128f9a8f0489")
    version("1.9.2", sha256="dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f")
    version("1.9.1", sha256="3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41")
    version("1.9.0", sha256="4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("python@3.0:", type=("build", "run"), when="@:1.9.3")
    depends_on("python@3.6:", type=("build", "run"), when="@1.9.4:")

    depends_on("py-setuptools")
    depends_on("py-hatchling")

    depends_on("py-numpy", type=("run"))
    depends_on("py-ase", when="@1.9.3", type=("run"))
    depends_on("py-matplotlib", when="@1.9.3", type=("run"))

    depends_on("py-scipy", when="@1.9.4:", type=("run"))

    for vers in ["1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "develop"]:
        depends_on("bigdft-futile@{0}".format(vers), type="run", when="@{0}".format(vers))

    build_directory = "PyBigDFT"

    patch("pyproject_fix.patch", when="@1.9.4")  # based on cb66dd0c4
    patch("bad_string.patch", when="@1.9.5")
