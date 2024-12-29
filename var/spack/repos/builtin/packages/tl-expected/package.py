# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TlExpected(CMakePackage):
    """C++11/14/17 std::expected with functional-style extensions."""

    homepage = "https://tl.tartanllama.xyz/en/latest/"
    url = "https://github.com/TartanLlama/expected/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/TartanLlama/expected.git"

    maintainers("charmoniumQ")

    license("CC0-1.0", checked_by="wdconinc")

    version("1.1.0", sha256="1db357f46dd2b24447156aaf970c4c40a793ef12a8a9c2ad9e096d9801368df6")
    with default_args(deprecated=True):
        # Note that the 1.0.0 has this issue:
        # https://github.com/TartanLlama/expected/issues/114
        # But no new patch version has been released,
        # so I will use the latest commit at the time of writing:
        version("2022-11-24", commit="b74fecd4448a1a5549402d17ddc51e39faa5020c")
    version("1.0.0", sha256="8f5124085a124113e75e3890b4e923e3a4de5b26a973b891b3deb40e19c03cee")

    depends_on("cxx", type="build")
