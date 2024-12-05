# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Etcd(Package):
    """etcd is a distributed reliable key-value store for the most
    critical data of a distributed system"""

    homepage = "https://etcd.io/"
    url = "https://github.com/etcd-io/etcd/archive/v3.4.7.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("3.5.9", sha256="ab24d74b66ba1ed7d2bc391839d961e7215f0f3d674c3a9592dad6dc67a7b223")
    version("3.4.23", sha256="055c608c4898d25f23aefbc845ff074bf5e8a07e61ed41dbd5cc4d4f59c93093")

    depends_on("go@1.19:")

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path("GOPATH", self.stage.path)

    def install(self, spec, prefix):
        make()
        install_tree("bin", prefix.bin)
