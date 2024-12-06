# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cachefilesd(MakefilePackage):
    """The cachefilesd daemon manages the caching files and directory that
    are that are used by network file systems such a AFS and NFS to do
    persistent caching to the local disk."""

    homepage = "https://people.redhat.com/~dhowells/fscache"
    url = "https://people.redhat.com/~dhowells/fscache/cachefilesd-0.10.tar.bz2"

    version("0.10.10", sha256="0d0309851efabd02b7c849f73535b8ad3f831570e83e4f65e42354da18e11a02")
    version("0.10.9", sha256="c897ec6704615f26de3ddc20ff30a191ce995cb8973d2cde88b4b28c1a1e6bca")
    version("0.10.7", sha256="193cca5efb37ee460a4ed8e1ed4878e3718e432ebe690ec4fe02486ef3f2494e")
    version("0.10.6", sha256="aaaaea887a5850c6fa01d09c80946e987411f6b550261f83967c671c65af959d")
    version("0.10.5", sha256="125ea4f6aef4bf8e936a7cc747b59e074537a8aed74cd1bab3f05d7fbc47287f")

    depends_on("c", type="build")  # generated

    @when("target=aarch64:")
    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter(r"-m64", "", string=True)

    def install(self, spec, prefix):
        make("DESTDIR={0}".format(prefix), "install")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
