# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmaxminddb(AutotoolsPackage):
    """C library for the MaxMind DB file format"""

    homepage = "https://github.com/maxmind/libmaxminddb"
    url = (
        "https://github.com/maxmind/libmaxminddb/releases/download/1.3.2/libmaxminddb-1.3.2.tar.gz"
    )

    license("Apache-2.0")

    version("1.9.1", sha256="a80682a89d915fdf60b35d316232fb04ebf36fff27fda9bd39fe8a38d3cd3f12")
    version("1.7.1", sha256="e8414f0dedcecbc1f6c31cb65cd81650952ab0677a4d8c49cab603b3b8fb083e")
    version("1.3.2", sha256="e6f881aa6bd8cfa154a44d965450620df1f714c6dc9dd9971ad98f6e04f6c0f0")

    depends_on("c", type="build")  # generated

    def configure_args(self):
        args = ["--disable-debug", "--disable-dependency-tracking", "--disable-silent-rules"]
        return args
