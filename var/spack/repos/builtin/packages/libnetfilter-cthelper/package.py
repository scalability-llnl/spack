# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibnetfilterCthelper(AutotoolsPackage):
    """Libnetfilter-cthelper library for user space helpers / ALGs"""

    homepage = "https://netfilter.org/projects/libnetfilter_cthelper/"
    url = "https://www.netfilter.org/projects/libnetfilter_cthelper/files/libnetfilter_cthelper-1.0.5.tar.bz2"

    license("GPL-2.0-or-later")

    version("1.0.1", sha256="14073d5487233897355d3ff04ddc1c8d03cc5ba8d2356236aa88161a9f2dc912")

    # Versions that were initially sourced at a third party are now deprecated
    with default_args(deprecated=True):
        # This appears to be version 1.0.0
        version(
            "1.2-2019Q4",
            sha256="15a7b13999d1428d75e720c8116318cd51bec1d365852ae1778d3c85b93a9777",
            url="https://github.com/vyos/libnetfilter-cthelper/archive/VyOS_1.2-2019Q4.tar.gz",
        )

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libmnl@1.0:")
