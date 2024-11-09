# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAwkwardCpp(PythonPackage):
    """py-awkward-cpp provides precompiled routines for the py-awkward package.
    It is not useful on its own, only as a dependency for py-awkward."""

    git = "https://github.com/scikit-hep/awkward.git"
    pypi = "awkward-cpp/awkward-cpp-9.tar.gz"
    homepage = "https://awkward-array.org"

    maintainers("vvolkl", "wdconinc")

    license("BSD-3-Clause")

    version("35", sha256="1f8b112a597bd2438794e1a721a63aa61869fa9598a17ac6bd811ad6f6400d06")
    version("12", sha256="429f7fcc37a671afa67fe9680f2edc3a123d1c74d399e5889c654f9529f9f8f2")
    version("11", sha256="02d719a4da7487564b29b8e8b78925a32ac818b6f5572c2f55912b4e0e59c7a4")
    version("10", sha256="d1c856cb6ef5cf3d4f67506a7efc59239f595635865cc9f4ab18440b8bfb11c6")
    version("9", sha256="db1c91c21f88b89a39b46176edc67a08b37f7283c16a2ed5159e3c874613c61a")
    version("8", sha256="a51b554490b3197fc5433822becb2e8208bf78fca82ffa314d839b72b3cc4169")
    version("7", sha256="dde733575b2a5ae5b946fe8667b4ae842d937d3b36ebb383d53dc53ea86ea65d")
    version("6", sha256="58e32afa8aa44c365e764f4b5d07637c79a79be2da7cfbaa3469d8bd26b0bfa2")
    version("5", sha256="e5d6a90d98a14dab36598015e69243b9f83b8851556104cbe778ca9c79923656")
    version("4", sha256="fbc4b5e552873e00ffb6286941efc7b629e4fbc4752e28afb9b54854128937f7")
    version("3", sha256="6070557762bd95d3642ad9c585609db51f899a1e79ce4f41568835efd7d6e066")
    version("2", sha256="5e63f43e3135f76db81e0924a74ecf4870f585c11a9f432568b377c04028868c")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"), when="@19:")
    depends_on("py-scikit-build-core@0.2.0:+pyproject", when="@11:", type="build")
    depends_on("py-pybind11", type=("build", "link"))
    depends_on("py-numpy@1.17.0:", when="@12:", type=("build", "run"))
    depends_on("py-numpy@1.18.0:", when="@19:", type=("build", "run"))

    # older versions
    depends_on("py-numpy@1.14.5:", when="@:11", type=("build", "run"))
    depends_on("py-scikit-build-core@0.1.3:+pyproject", when="@:9", type="build")

    # https://github.com/scikit-hep/awkward/issues/3132#issuecomment-2136042870
    conflicts("%gcc@14:", when="@:33")
