# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tiptop(AutotoolsPackage):
    """Tiptop is a performance monitoring tool for Linux."""

    homepage = "https://github.com/FeCastle/tiptop"
    git = "https://github.com/FeCastle/tiptop.git"

    license("GPL-2.0")

    version("master", commit="529886d445ec32febad14246245372a8f244b3eb")

    depends_on("c", type="build")  # generated

    depends_on("papi")
    depends_on("byacc", type="build")
    depends_on("flex", type="build")

    patch("NR_perf_counter_open_aarch64.patch", when="target=aarch64:")
