# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kumi(CMakePackage):
    """KUMI - C++20 Tuple & Tuple-base Algorithms Library."""

    homepage = "https://jfalcou.github.io/kumi/"
    url = "https://github.com/jfalcou/kumi/archive/refs/tags/v3.0.tar.gz"
    maintainers("jfalcou")
    git = "https://github.com/jfalcou/kumi.git"

    license("BSL-1.0")

    version("main", branch="main")
    version("3.0", sha256="166b621e475935d2a3a195d13937a285060812c1fd7a95575a9c7b1dc425f2a1")
    version("2.1", sha256="34fc756780d463db35716e40eecd89b1505917926281262c74af425556a5260c")
    version("2.0", sha256="c9f2d2014d3513c57db4457c5a678c7adce1fa9bd061ee008847876f06dac355")
    version("1.0", sha256="d28be244e326b1c9f1651b47728af74bb6be80a7accd39f07441a246d49220f5")

    depends_on("cxx", type="build")  # generated
