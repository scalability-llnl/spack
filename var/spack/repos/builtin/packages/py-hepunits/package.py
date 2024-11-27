# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepunits(PythonPackage):
    """Units and constants in the HEP system of units."""

    git = "https://github.com/scikit-hep/hepunits.git"
    pypi = "hepunits/hepunits-1.2.1.tar.gz"
    homepage = "https://github.com/scikit-hep/hepunits"

    tags = ["hep"]

    maintainers("vvolkl")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2.3.2", sha256="8a3366fa5d72c16af1166ed579cdaa81edd2676acb8f6a1fe7da290cefca3b08")
    version("2.3.1", sha256="b1174bba4d575b9939c01f341e24d9bdbe0e0cd4cc4ce2e7d77692da19145cfb")
    version("2.3.0", sha256="33b9ae9a8b7b3af355141a74901cb5aa557dce2e4c9992a0a30ef0443a1b2206")
    version("2.2.1", sha256="6097e69547a483bdc0cfe4d106e447b5eba87c5501060d312cd9d61aa9e22414")
    version("2.2.0", sha256="e80e616fef2817f3c66c75dc0e41ed26362488cce05f94adcfdefb8e05ebcb58")
    version("2.1.3", sha256="68449b0c7b7fe133023da71c3486901080966a4be6cc4ac48d7dd41d087fa130")
    version("2.1.2", sha256="a77e2f28d4a54a9abae4ea1e86c565783971a0b99bc0678eab3fe47b2224d377")
    version("2.1.1", sha256="21b18bbf82ade5e429e2c71ec41bc5ae8005b275466bdaef0159ddc4f8085b31")
    version("2.1.0", sha256="9e8da814c242579ad1fde6ccff0514195c70ab6d232eab8ff0ad675239686ef6")
    version("1.2.1", sha256="b05b0dda32bf797806d506d7508d4eb23b78f34d67bbba9348a2b4a9712666fa")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("python@3.6:", when="@2.2:", type=("build", "run"))
    depends_on("python@3.7:", when="@2.3:", type=("build", "run"))
    depends_on("py-setuptools", when="@:2.2", type="build")
    depends_on("py-setuptools-scm +toml", when="@:2.2", type="build")
    depends_on("py-hatchling", when="@2.3:", type="build")
    depends_on("py-hatch-vcs", when="@2.3:", type="build")
    depends_on("py-toml", when="@:2.1.1", type="build")
