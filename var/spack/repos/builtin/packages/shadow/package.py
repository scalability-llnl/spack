# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shadow(AutotoolsPackage):
    """Tools to help unprivileged users create uid and gid mappings in
    user namespaces."""

    homepage = "https://github.com/shadow-maint/shadow"
    url = "https://github.com/shadow-maint/shadow/releases/download/4.7/shadow-4.7.tar.gz"
    git = "https://github.com/shadow-maint/shadow.git"

    license("BSD-3-Clause")

    version("4.16.0", sha256="1744f339e07a2b41056347ddd612839762ff565d7e9494fb049428002fa2e7e0")
    version("4.15.1", sha256="b34686b89b279887ffbf1f33128902ccc0fa1a998a3add44213bb12d7385b218")
    version("4.13", sha256="813057047499c7fe81108adcf0cffa3ad4ec75e19a80151f9cbaa458ff2e86cd")
    version("4.8.1", sha256="3ee3081fbbcbcfea5c8916419e46bc724807bab271072104f23e7a29e9668f3a")
    version("4.7", sha256="5135b0ca2a361a218fab59e63d9c1720d2a8fc1faa520c819a654b638017286f")
    version("4.6", sha256="4668f99bd087399c4a586084dc3b046b75f560720d83e92fd23bf7a89dda4d31")

    depends_on("c", type="build")

    def configure_args(self):
        # Fix build when libbsd is not installed on the host:
        return ["--without-libbsd"]
