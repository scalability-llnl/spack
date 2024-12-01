# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JxrlibDebian(MakefilePackage):
    """JPEG XR is a still image format based on technology originally
    developed by Mirosoft under the name HD Photo
    (formerly Windows Media Photo). The JPEG XR format is similar,
    but not identical, to the HD Photo/Windows Media Photo format."""

    homepage = "https://packages.debian.org/source/sid/jxrlib"
    url = "https://salsa.debian.org/debian-phototools-team/jxrlib/-/archive/debian/1.2_git20170615.f752187-5/jxrlib-debian-1.2_git20170615.f752187-5.tar.gz"

    variant("shared", default=False, description="Build shared libs")

    license("BSD-2-Clause")

    version(
        "1.2_git20170615.f752187-5",
        sha256="3d9d5d6ca972b51259efe1f37a8e42892e90920b13308d70b8a24eb9a82bf34c",
    )

    depends_on("c", type="build")  # generated

    def setup_build_environment(self, env):
        env.set("DIR_INSTALL", self.prefix)
        if self.spec.satisfies("+shared"):
            env.set("SHARED", "True")
