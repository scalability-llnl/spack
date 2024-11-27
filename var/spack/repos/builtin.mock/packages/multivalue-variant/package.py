# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MultivalueVariant(Package):
    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("2.1", md5="0123456789abcdef0123456789abcdef")
    version("2.2", md5="0123456789abcdef0123456789abcdef")
    version("2.3", md5="0123456789abcdef0123456789abcdef")

    variant("debug", default=False, description="Debug variant")
    variant(
        "foo",
        description="Multi-valued variant",
        values=any_combination_of("bar", "baz", "barbaz", "fee"),
    )

    variant(
        "fee",
        description="Single-valued variant",
        default="bar",
        values=("bar", "baz", "barbaz"),
        multi=False,
    )

    variant(
        "libs",
        default="shared",
        values=("shared", "static"),
        multi=True,
        description="Type of libraries to install",
    )

    depends_on("mpi")
    depends_on("callpath")
    depends_on("pkg-a")
    depends_on("pkg-a@1.0", when="fee=barbaz")
