# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CppLogger(CMakePackage):
    """A simple C++ logger"""

    homepage = "https://github.com/hariharan-devarajan/cpp-logger"
    git = "https://github.com/hariharan-devarajan/cpp-logger.git"
    maintainers("hariharan-devarajan")

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("0.0.4", tag="v0.0.4", commit="2231deee4b74fb1ddae3dae0618baaead4fecf75")
    version("0.0.3", tag="v0.0.3", commit="398e6fa1eb4442cba94d46ecacfa47a426474387")
    version("0.0.2", tag="v0.0.2", commit="329a48401033d2d2a1f1196141763cab029220ae")
    version("0.0.1", tag="v0.0.1", commit="d48b38ab14477bb7c53f8189b8b4be2ea214c28a")

    depends_on("cxx", type="build")  # generated
