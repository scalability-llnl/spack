# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJpype1(PythonPackage):
    """JPype is an effort to allow python programs full access to java class
    libraries."""

    homepage = "https://github.com/originell/jpype"
    pypi = "JPype1/JPype1-0.6.2.tar.gz"

    version("0.6.3", sha256="6841523631874a731e1f94e1b1f130686ad3772030eaa3b6946256eeb1d10dd1")
    version("0.6.2", sha256="99206412d80b9d5a81a7cc205267ca63554403eb57f13420302e2f39bfad7f25")
    version("0.6.1", sha256="0d366228b7b37b0266184161cc7ea1ce58f60199f6ec9451985149ea873774be")
    version("0.6.0", sha256="f5d783520cb4c30595c3bc509065e30fc292ec7cfb57045141eae77c518bcdb0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("numpy", default=False, description="Build numpy extensions")

    depends_on("python@2.6:")

    depends_on("py-setuptools", type="build")
    depends_on("java", type=("build", "run"))
    # extra requirements
    depends_on("py-numpy@1.6:", type=("build", "run"), when="+numpy")
