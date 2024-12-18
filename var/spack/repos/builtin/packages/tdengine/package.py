# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tdengine(CMakePackage):
    """An open-source big data platform designed and optimized for the
    Internet of Things (IoT)."""

    homepage = "https://github.com/taosdata/TDengine"
    url = "https://github.com/taosdata/TDengine/archive/ver-2.0.2.2.tar.gz"

    license("AGPL-3.0-only")

    version("2.0.3.2", sha256="3eb8df894998d5592cce377b4f7e267972aee8adf9fc1ce60d1af532ffa9c1c6")
    version("2.0.3.1", sha256="69418815afcac8051f1aab600415669003b4aeec4ec2aaf09cab24636edaf51f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    @when("target=aarch64:")
    def cmake_args(self):
        args = ["-DCPUTYPE=aarch64"]
        return args

    def install(self, spec, prefix):
        install_tree(self.build_directory + "/build", prefix)
