# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exempi(AutotoolsPackage):
    """exempi is a port of Adobe XMP SDK to work on UNIX and to be build with
    GNU automake.

    It includes XMPCore and XMPFiles, libexempi, a C-based API and exempi
    a command line tool.
    """

    homepage = "https://libopenraw.freedesktop.org/wiki/Exempi"
    url = "https://libopenraw.freedesktop.org/download/exempi-2.6.1.tar.bz2"

    license("BSD-3-Clause")

    version("2.6.1", sha256="072451ac1e0dc97ed69a2e5bfc235fd94fe093d837f65584d0e3581af5db18cd")
    version("2.5.2", sha256="52f54314aefd45945d47a6ecf4bd21f362e6467fa5d0538b0d45a06bc6eaaed5")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("iconv")
    # needs +test variant to prevent following error:
    # 118    checking for the Boost unit_test_framework library... no
    # >> 119    configure: error: cannot find the flags to link with Boost
    #           unit_test_framework
    depends_on("boost+test@1.79.0:", when="@2.6.1:")
    depends_on("boost+test@1.48.0:")
    depends_on("pkgconfig")
    depends_on("expat")

    conflicts("%gcc@:4.5")

    def configure_args(self):
        args = ["--with-boost={0}".format(self.spec["boost"].prefix)]

        if self.spec.satisfies("platform=darwin"):
            args += ["--with-darwinports", "--with-fink"]

        return args
