# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xtl(CMakePackage):
    """QuantStack tools library"""

    homepage = "https://github.com/QuantStack/xtl"
    url = "https://github.com/QuantStack/xtl/archive/0.3.4.tar.gz"
    git = "https://github.com/QuantStack/xtl.git"

    maintainers("ax3l")

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("0.7.4", sha256="3c88be0e696b64150c4de7a70f9f09c00a335186b0b0b409771ef9f56bca7d9a")
    version("0.7.2", sha256="95c221bdc6eaba592878090916383e5b9390a076828552256693d5d97f78357c")
    version("0.6.4", sha256="5db5087c37daab3e1d35337782f79972aaaf19218a0de786a0515f247244e390")
    version("0.4.0", sha256="2cfe9acbcc4e484f3aa33a98892a09ffe79bb9c0dfd3ffc57b3561f44c591e7c")
    version("0.3.4", sha256="618536c3998091b0bdd7f8202e8bec9c34e82409c8ee0ea179a2759bdea426e2")
    version("0.3.3", sha256="1110364c2ea0a2536ec6673e46afcb8fa7e92a66593211270bbeb26b85342600")

    depends_on("cxx", type="build")  # generated

    # C++14 support
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.6")
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')
