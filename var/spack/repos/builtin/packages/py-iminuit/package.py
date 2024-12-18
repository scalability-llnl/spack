# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIminuit(PythonPackage):
    """Interactive IPython-Friendly Minimizer based on SEAL Minuit2."""

    pypi = "iminuit/iminuit-1.2.tar.gz"

    version("2.8.4", sha256="4b09189f3094896cfc68596adc95b7f1d92772e1de1424e5dc4dd81def56e8b0")
    version("1.5.2", sha256="0b54f4d4fc3175471398b573d24616ddb8eb7d63808aa370cfc71fc1d636a1fd")
    version("1.3.7", sha256="9173e52cc4a0c0bda13ebfb862f9b074dc5de345b23cb15c1150863aafd8a26c")
    version("1.3.6", sha256="d79a197f305d4708a0e3e52b0a6748c1a6997360d2fbdfd09c022995a6963b5e")
    version("1.2", sha256="7651105fc3f186cfb5742f075ffebcc5088bf7797d8ed124c00977eebe0d1c64")

    depends_on("cxx", type="build")  # generated

    # Required dependencies
    depends_on("python@3.6:", type=("build", "run"), when="@2.6.1:")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"), when="@1.3:1.3.6")
    depends_on("py-numpy@1.11.3:", type=("build", "run"), when="@1.3.7:")
    # https://github.com/numpy/numpy/issues/26191#issuecomment-2179127999
    depends_on("py-numpy@:1", when="@:2.25", type=("build", "run"))
    depends_on("cmake", type="build", when="@2.8.4")
