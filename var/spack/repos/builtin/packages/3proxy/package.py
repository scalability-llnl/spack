# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class _3proxy(MakefilePackage):
    """3proxy - tiny free proxy server"""

    homepage = "https://3proxy.org"
    url = "https://github.com/z3APA3A/3proxy/archive/0.8.13.tar.gz"

    version("0.8.13", sha256="a6d3cf9dd264315fa6ec848f6fe6c9057db005ce4ca8ed1deb00f6e1c3900f88")
    version("0.8.12", sha256="c2ad3798b4f0df06cfcc7b49f658304e451d60e4834e2705ef83ddb85a03f849")
    version("0.8.11", sha256="fc4295e1a462baa61977fcc21747db7861c4e3d0dcca86cbaa3e06017e5c66c9")

    depends_on("c", type="build")

    def build(self, spec, prefix):
        make("-f", f"Makefile.{platform.system()}", f"CC={spack_cc}", f"LN={spack_cc}")

    def install(self, spec, prefix):
        make(
            "-f",
            f"Makefile.{platform.system()}",
            f"prefix={prefix}",
            f"CC={spack_cc}",
            f"LN={spack_cc}",
            "install",
        )
