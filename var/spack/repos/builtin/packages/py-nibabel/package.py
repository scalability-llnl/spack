# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNibabel(PythonPackage):
    """Access a multitude of neuroimaging data formats"""

    homepage = "https://nipy.org/nibabel"
    pypi = "nibabel/nibabel-3.2.1.tar.gz"
    git = "https://github.com/nipy/nibabel"

    maintainers("ChristopherChristofi")

    # As detailed: https://nipy.org/nibabel/legal.html
    license("MIT AND BSD-3-Clause AND PSF-2.0 AND PDDL-1.0")

    version("5.2.1", sha256="b6c80b2e728e4bc2b65f1142d9b8d2287a9102a8bf8477e115ef0d8334559975")
    version("5.1.0", sha256="ce73ca5e957209e7219a223cb71f77235c9df2acf4d3f27f861ba38e9481ac53")
    version("4.0.2", sha256="45c49b5349351b45f6c045a91aa02b4f0d367686ff3284632ef95ac65b930786")
    version("3.2.2", sha256="b0dcc174b30405ce9e8fec1eab3cbbb20f5c5e4920976c08b22e050b7c124f94")
    version("3.2.1", sha256="4d2ff9426b740011a1c916b54fc25da9348282e727eaa2ea163f42e00f1fc29e")
    version("2.4.1", sha256="f165ff1cb4464902d6594eb2694e2cfb6f8b9fe233b856c976c3cff623ee0e17")

    depends_on("python@3.8:", when="@5:", type=("build", "run"))
    depends_on("python@3.7:", when="@4:", type=("build", "run"))
    depends_on("py-hatchling", when="@5:", type="build")
    depends_on("py-hatch-vcs", when="@5:", type="build")

    depends_on("py-numpy@1.20:", when="@5.2.1:", type=("build", "run"))
    depends_on("py-numpy@1.19:", when="@5:", type=("build", "run"))
    depends_on("py-numpy@1.17:", when="@4:", type=("build", "run"))
    depends_on("py-numpy@1.14:", when="@3.2:", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-packaging@17:", when="@4:", type=("build", "run"))
    depends_on("py-packaging@14.3:", when="@3.1:", type=("build", "run"))
    depends_on("py-importlib-resources@1.3:", when="@5.2.1: ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-resources@1.3:", when="@5.1: ^python@:3.8", type=("build", "run"))

    depends_on("py-pytest", type="test")

    # Historical dependencies
    depends_on("py-setuptools@30.3.0:", when="@:5.0", type=("build", "run"))
    depends_on("py-six@1.3:", when="@:2.5", type=("build", "run"))
