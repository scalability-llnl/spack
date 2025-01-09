# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibnetfilterCttimeout(AutotoolsPackage):
    """Conntrack timeout policy library."""

    homepage = "https://netfilter.org/projects/libnetfilter_cttimeout/"
    url = "https://www.netfilter.org/projects/libnetfilter_cttimeout/files/libnetfilter_cttimeout-1.0.1.tar.bz2"

    license("GPL-2.0-only", checked_by="wdconinc")

    version("1.0.1", sha256="0b59da2f3204e1c80cb85d1f6d72285fc07b01a2f5678abf5dccfbbefd650325")

    # Versions that were initially sourced at a third party are now deprecated
    with default_args(deprecated=True):
        # This appears to be version 1.0.0
        version(
            "1.2-2019Q4",
            sha256="71cebdf07a578901b160a54199062a4b4cd445e14742e2c7badc0900d8ae56b6",
            url="https://github.com/vyos/libnetfilter-cttimeout/archive/VyOS_1.2-2019Q4.tar.gz",
        )

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libmnl")
