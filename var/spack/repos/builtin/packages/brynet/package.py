# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brynet(CMakePackage):
    """Header Only Cross platform high performance TCP network library
    using C++ 11."""

    homepage = "https://github.com/IronsDu/brynet"
    url = "https://github.com/IronsDu/brynet/archive/v1.0.8.tar.gz"

    license("MIT")

    version("1.12.2", sha256="b8b740cae39804d1e7037866046321065856c0ea9f565d26f67aeccc7ccd3d51")
    version("1.10.0", sha256="a7bc20c4a2cc2f0f29af56e9355b8769256785850ddedcef226e9562e97d05cf")
    version("1.0.8", sha256="e37dee5fa14acec99bdd7ce8530a00ff5116f608f0a5401cd2e32e10f23975fc")
    version("1.0.7", sha256="60116fccff108d03f3ff0a3d5c1fb5ad442bad7ef155bf1a3c7819ffc9d57524")
    version("1.0.6", sha256="5e94b5b64fbdfbcb4e33b11fb7832cf0ca3898ab6b6461867182598bab7ca65f")

    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        args = []
        args.append("-Dbrynet_BUILD_EXAMPLES=ON")
        args.append("-Dbrynet_BUILD_TESTS=ON")
        return args
