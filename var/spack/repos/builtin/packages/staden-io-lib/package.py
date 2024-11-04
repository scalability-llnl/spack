# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class StadenIoLib(AutotoolsPackage):
    """Io_lib is a library for reading/writing various bioinformatics
    file formats."""

    homepage = "https://github.com/jkbonfield/io_lib"

    license("BSD-3-Clause")

    maintainers("snehring")

    version("1.15.0", sha256="ad343dac7c77086db1b54585c5887b26eda6430d1639d111dd3304c3b749494f")
    version("1.14.9", sha256="8d0732f3d37abba1633731bfacac5fd7f8172eccb1cef224e8ced904d3b242f4")
    version(
        "1.14.8",
        sha256="3bd560309fd6d70b14bbb8230e1baf8706b804eb6201220bb6c3d6db72003d1b",
        url="https://sourceforge.net/projects/staden/files/io_lib/1.14.8/io_lib-1.14.8.tar.gz/download",
    )

    depends_on("c", type="build")

    variant("libdeflate", default=False, description="Build with libdeflate")
    variant("curl", default=False, description="Build with curl support")
    variant("shared", default=True, description="Build shared libraries")

    depends_on("zlib-api", when="~libdeflate")
    depends_on("libdeflate", when="+libdeflate")
    depends_on("bzip2")
    depends_on("xz")
    depends_on("curl", when="+curl")

    def url_for_version(self, version):
        return f"https://github.com/jkbonfield/io_lib/releases/download/io_lib-{version.dashed}/io_lib-{version.dotted}.tar.gz"

    def configure_args(self):
        args = self.enable_or_disable("shared")

        if self.spec.satisfies("~curl"):
            args.append("--without-libcurl")

        return args
