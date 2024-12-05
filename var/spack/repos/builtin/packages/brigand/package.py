# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Brigand(CMakePackage):
    """Brigand Meta-programming library"""

    homepage = "https://github.com/edouarda/brigand"
    url = "https://github.com/edouarda/brigand/archive/1.0.0.tar.gz"
    git = "https://github.com/edouarda/brigand.git"

    maintainers("nilsvu")

    license("BSL-1.0")

    version("master", branch="master")
    version("1.3.0", sha256="2468107c5b9ab0b56d84797dfc6636d0aae0507ae9cd6cb1acc1de85e5787acd")
    version("1.2.0", sha256="4287fa7278cc000a63e90f1a1b903952b7f606b1a3cf95c23a422d2fe96ca50d")
    version("1.1.0", sha256="afdcc6909ebff6994269d3039c31698c2b511a70280072f73382b26855221f64")
    version("1.0.0", sha256="8daf7686ff39792f851ef1977323808b80aab31c5f38ef0ba4e6a8faae491f8d")

    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        args = [self.define("BUILD_TESTING", self.run_tests)]
        return args
