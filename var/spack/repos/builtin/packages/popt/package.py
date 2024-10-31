# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Popt(AutotoolsPackage):
    """The popt library parses command line options."""

    homepage = "https://github.com/rpm-software-management/popt"
    url = "https://ftp.osuosl.org/pub/rpm/popt/releases/popt-1.x/popt-1.19.tar.gz"

    license("MIT")

    version("1.19", sha256="c25a4838fc8e4c1c8aacb8bd620edb3084a3d63bf8987fdad3ca2758c63240f9")
    version("1.16", sha256="e728ed296fe9f069a0e005003c3d6b2dde3d9cad453422a10d6558616d304cc8")

    depends_on("c", type="build")

    depends_on("iconv")

    def url_for_version(self, version):
        if self.spec.satisfies("@1.18:"):
            return f"https://ftp.osuosl.org/pub/rpm/popt/releases/popt-{version.up_to(1)}.x/popt-{version}.tar.gz"
        else:
            return f"https://launchpad.net/popt/head/{version}/+download/popt-{version}.tar.gz"

    def patch(self):
        # Remove flags not recognized by the NVIDIA compilers
        if self.spec.satisfies("%nvhpc@:20.11"):
            filter_file(
                'CFLAGS="$CFLAGS -Wall -W"', 'CFLAGS="$CFLAGS -Wall"', "configure", string=True
            )
