# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class CRaft(AutotoolsPackage):
    """C implementation of the Raft consensus protocol."""

    homepage = "https://raft.readthedocs.io/en/latest/"
    git = "https://github.com/canonical/raft.git"
    url = "https://github.com/canonical/raft/archive/refs/tags/v0.17.1.tar.gz"

    maintainers("mdorier")

    version("master", branch="master")
    version("0.17.1", sha256="e31c7fafbdd5f94913161c5d64341a203364e512524b47295c97a91e83c4198b")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    variant("uv", default=True, description="Enable libuv support")

    depends_on("libuv@1.18.0:", when="+uv")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = ["--disable-lz4"]
        args += self.enable_or_disable("uv")
        return args
