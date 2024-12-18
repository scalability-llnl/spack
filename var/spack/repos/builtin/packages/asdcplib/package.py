# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Asdcplib(AutotoolsPackage):
    """AS-DCP and AS-02 File Access Library."""

    homepage = "https://github.com/cinecert/asdcplib"
    url = "https://github.com/cinecert/asdcplib/archive/rel_2_10_35.tar.gz"

    license("AMPAS")

    version("2_10_38", sha256="f8cb3b1fecfe18f1a64e12e96e5696480631509e9088e29f5a259eb25b1b1656")
    version("2_10_35", sha256="a68eec9ae0cc363f75331dc279c6dd6d3a9999a9e5f0a4405fd9afa8a29ca27b")
    version("2_10_34", sha256="faa54ee407c1afceb141e08dae9ebf83b3f839e9c49a1793ac741ec6cdee5c3c")
    version("2_10_33", sha256="16fafb5da3d46b0f44570ef9780c85dd82cca60106a9e005e538809ea1a95373")
    version("2_10_32", sha256="fe5123c49980ee3fa25dea876286f2ac974d203bfcc6c77fc288a59025dee3ee")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("openssl", type=("build", "link"))

    def configure_args(self):
        spec = self.spec

        args = [f"--with-openssl={spec['openssl'].prefix}"]

        return args
