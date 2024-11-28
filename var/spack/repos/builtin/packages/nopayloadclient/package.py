# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nopayloadclient(CMakePackage):
    """NoPayloadClient is the client-side library meant to communicate with NoPayloadDB."""

    homepage = "https://github.com/BNLNPPS/nopayloadclient"
    url = "https://github.com/BNLNPPS/nopayloadclient/archive/refs/tags/v0.0.3.tar.gz"
    git = "https://github.com/BNLNPPS/nopayloadclient.git"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("main", branch="main")
    version("0.0.3", sha256="9481981d0cfbe1727f08ae3d1129c142a952d5e67ddb9ad88224356040af2225")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("curl")
    depends_on("nlohmann-json", type="build")

    def cmake_args(self):
        return [
            self.define("BUILD_TESTING", self.run_tests),
            self.define("INCLUDE_DIR_NLOHMANN_JSON", self.spec["nlohmann-json"].prefix.include),
        ]
