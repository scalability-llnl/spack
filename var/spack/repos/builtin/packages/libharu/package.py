# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Libharu(AutotoolsPackage):
    """libharu - free PDF library.

    Haru is a free, cross platform, open-sourced software library for
    generating PDF."""

    homepage = "http://libharu.org"
    url = "https://github.com/libharu/libharu/archive/RELEASE_2_3_0.tar.gz"
    git = "https://github.com/libharu/libharu.git"

    license("custom")

    version("master", branch="master")
    version("2.3.0", sha256="8f9e68cc5d5f7d53d1bc61a1ed876add1faf4f91070dbc360d8b259f46d9a4d2")
    version("2.2.0", sha256="5e63246d2da0272a9dbe5963fd827c7efa6e29d97a2d047c0d4c5f0b780f10b5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libtool", type=("build"))
    depends_on("autoconf", type=("build"))
    depends_on("automake", type=("build"))
    depends_on("libpng")
    depends_on("zlib-api")

    def autoreconf(self, spec, prefix):
        """execute their autotools wrapper script"""
        if os.path.exists("./buildconf.sh"):
            bash = which("bash")
            bash("./buildconf.sh", "--force")

    def configure_args(self):
        """Point to spack-installed zlib and libpng"""
        spec = self.spec
        args = []

        args.append(f"--with-zlib={spec['zlib-api'].prefix}")
        args.append(f"--with-png={spec['libpng'].prefix}")

        return args

    def url_for_version(self, version):
        url = "https://github.com/libharu/libharu/archive/RELEASE_{0}.tar.gz"
        return url.format(version.underscored)
