# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libffs(CMakePackage):
    """FFS is a middleware library for data communication,
    including representation, processing and marshaling
    that preserves the performance of traditional approaches
    while relaxing the requirement of a priori knowledge
    and providing complex run-time flexibility.
    """

    homepage = "https://www.cc.gatech.edu/systems/projects/FFS"
    url = "https://github.com/GTkorvo/ffs/archive/v1.1.tar.gz"
    git = "https://github.com/GTkorvo/ffs.git"

    version("develop", branch="master")
    version("1.5", sha256="e1f3df42eb36fa35c5445887d679e26b7e3c9be697a07cd38e4ae824dbcd8ef8")
    version("1.1.1", sha256="9c3a82b3357e6ac255b65d4f45003dd270dea3ec0cd7a2aa40b59b3eab4bdb83")
    version("1.1", sha256="008fd87c5a6cb216cd757b4dc04057fc987b39b7a367623eb4cf0fd32a9fd81e")

    depends_on("c", type="build")  # generated

    depends_on("flex", type="build", when="@:1.4")
    depends_on("bison", type="build", when="@:1.4")
    depends_on("gtkorvo-cercs-env", type="build", when="@:1.4")
    depends_on("gtkorvo-atl")
    depends_on("gtkorvo-dill")

    def cmake_args(self):
        args = ["-DTARGET_CNL=1"]
        if self.spec.satisfies("@1.5:"):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append("-DENABLE_TESTING=0")
        else:
            args.append("-DENABLE_TESTING=0")

        return args
