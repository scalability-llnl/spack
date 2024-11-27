# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibnetfilterQueue(AutotoolsPackage):
    """Libnetfilter-queue libnetfilter queue library."""

    homepage = "https://netfilter.org/projects/libnetfilter_queue/"
    url = "https://www.netfilter.org/projects/libnetfilter_queue/files/libnetfilter_queue-1.0.5.tar.bz2"

    license("GPL-2.0-only")

    version("1.0.5", sha256="f9ff3c11305d6e03d81405957bdc11aea18e0d315c3e3f48da53a24ba251b9f5")

    # Versions that were initially sourced at a third party are now deprecated
    with default_args(deprecated=True):
        # This appears to be version 1.0.2
        version(
            "1.2-2019Q4",
            sha256="73b87e600b492cf9e3aa8fb6e9855e1ccc523a7bc466c1fd1a0e6ffa424d746e",
            url="https://github.com/vyos/libnetfilter-queue/archive/VyOS_1.2-2019Q4.tar.gz",
        )

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libnfnetlink")
    depends_on("libmnl@1.0.3:")
