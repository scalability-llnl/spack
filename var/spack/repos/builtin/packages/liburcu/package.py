# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liburcu(AutotoolsPackage):
    """liburcu is a LGPLv2.1 userspace RCU (read-copy-update) library.
    This data synchronization library provides read-side access which
    scales linearly with the number of cores."""

    homepage = "https://liburcu.org"
    url = "https://lttng.org/files/urcu/userspace-rcu-0.14.0.tar.bz2"
    git = "https://git.lttng.org/userspace-rcu.git"

    license("LGPL-2.1", checked_by="wdconinc")

    version("0.14.0", sha256="ca43bf261d4d392cff20dfae440836603bf009fce24fdc9b2697d837a2239d4f")

    depends_on("autoconf@2.69:", type="build")
    depends_on("automake@1.12:", type="build")

    def patch(self):
        filter_file("-Wl,-rpath ", "-Wl,-rpath,", "doc/examples/Makefile.in")
