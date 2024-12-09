# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmaus2(AutotoolsPackage):
    """libmaus2 is a collection of data structures and algorithmse."""

    homepage = "https://gitlab.com/german.tischler/libmaus2"
    url = "https://gitlab.com/german.tischler/libmaus2/-/archive/2.0.767-release-20201123131410/libmaus2-2.0.767-release-20201123131410.tar.gz"

    version(
        "2.0.767",
        sha256="40cec9bef2fb61d8df0a35cdf76c59a1d8389686d393805138c364d0c029f03c",
        url="https://gitlab.com/german.tischler/libmaus2/-/archive/2.0.767-release-20201123131410/libmaus2-2.0.767-release-20201123131410.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    conflicts(
        "%gcc@:7.9",
        msg=(
            "libmaus2 uses std::filesystem. "
            "std::filesystem requires greater than or equal to GCC 8."
        ),
    )

    def setup_build_environment(self, env):
        if self.spec.satisfies("%gcc@8.0:8.9") or self.spec.satisfies("%fj"):
            env.append_flags("LDFLAGS", "-lstdc++fs")
