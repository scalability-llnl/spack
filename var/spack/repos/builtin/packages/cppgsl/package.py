# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppgsl(CMakePackage):
    """C++ Guideline Support Library"""

    homepage = "https://github.com/Microsoft/GSL"
    url = "https://github.com/Microsoft/GSL/archive/v2.0.0.tar.gz"
    git = "https://github.com/Microsoft/GSL.git"

    license("MIT")

    version("main", branch="main")
    version("4.0.0", sha256="f0e32cb10654fea91ad56bde89170d78cfbf4363ee0b01d8f097de2ba49f6ce9")
    version("3.1.0", sha256="d3234d7f94cea4389e3ca70619b82e8fb4c2f33bb3a070799f1e18eef500a083")
    version("2.1.0", sha256="ef73814657b073e1be86c8f7353718771bf4149b482b6cb54f99e79b23ff899d")
    version("2.0.0", sha256="6cce6fb16b651e62711a4f58e484931013c33979b795d1b1f7646f640cfa9c8e")
    version("1.0.0", sha256="9694b04cd78e5b1a769868f19fdd9eea2002de3d4c3a81a1b769209364543c36")

    depends_on("cxx", type="build")  # generated

    variant(
        "cxxstd",
        default="14",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake@3.1.3:", type="build")

    def cmake_args(self):
        return [
            self.define_from_variant("GSL_CXX_STANDARD", "cxxstd"),
            self.define("GSL_TEST", self.run_tests),
        ]
