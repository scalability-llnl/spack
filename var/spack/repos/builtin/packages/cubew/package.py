# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cubew(AutotoolsPackage):
    """Component of CubeBundle: High performance C Writer library"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.4/dist/cubew-4.4.tar.gz"

    maintainers("swat-jsc", "wrwilliams")

    version("4.8.2", sha256="4f3bcf0622c2429b8972b5eb3f14d79ec89b8161e3c1cc5862ceda417d7975d2")
    version("4.8.1", sha256="42cbd743d87c16e805c8e28e79292ab33de259f2cfba46f2682cb35c1bc032d6")
    version("4.8", sha256="73c7f9e9681ee45d71943b66c01cfe675b426e4816e751ed2e0b670563ca4cf3")
    version("4.7.1", sha256="0d364a4930ca876aa887ec40d12399d61a225dbab69e57379b293516d7b6db8d")
    version("4.7", sha256="a7c7fca13e6cb252f08d4380223d7c56a8e86a67de147bcc0279ebb849c884a5")
    version("4.6", sha256="99fe58ce7ab13061ebfbc360aedaecc28099a30636c5269a42c0cbaf57149aa8")
    version(
        "4.5",
        sha256="16bd8fd864197a74ca65f7325761ad75d73d555072326e95e1338cff39f28a5c",
        deprecated="true",
    )
    version(
        "4.4.3",
        sha256="93fff6cc1e8b0780f0171ef5302a2e1a257f99b6383fbfc1b9b82f925ceff501",
        deprecated="true",
    )
    version(
        "4.4.2",
        sha256="31a71e9a05e6523de2b86b4026821bbb75fb411eb5b18ae38b27c1f44158014a",
        deprecated="true",
    )
    version(
        "4.4.1",
        sha256="c09e3f5a3533ebedee2cc7dfaacd7bac4680c14c3fa540669466583a23f04b67",
        deprecated="true",
    )
    version(
        "4.4",
        sha256="b1d6fecb546bc645ced430ea3fc166e85835f3b997d4e5f0dece71919fc95a99",
        deprecated="true",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("zlib-api")

    def url_for_version(self, version):
        url = "http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cubew-{1}.tar.gz"

        return url.format(version.up_to(2), version)

    def configure_args(self):
        configure_args = ["--enable-shared"]
        configure_args.append("--with-frontend-zlib=%s" % self.spec["zlib-api"].prefix.lib)
        configure_args.append("--with-backend-zlib=%s" % self.spec["zlib-api"].prefix.lib)

        return configure_args

    def install(self, spec, prefix):
        make("install", parallel=True)
