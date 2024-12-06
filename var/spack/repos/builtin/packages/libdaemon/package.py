# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdaemon(AutotoolsPackage):
    """libdaemon is a lightweight C library which eases the writing of
    UNIX daemons."""

    homepage = "https://0pointer.de/lennart/projects/libdaemon/"
    url = "https://0pointer.de/lennart/projects/libdaemon/libdaemon-0.14.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.14", sha256="fd23eb5f6f986dcc7e708307355ba3289abe03cc381fc47a80bca4a50aa6b834")
    version("0.13", sha256="bd949d459d2da54f1cdfbd1f4592e32541e8a195aca56fa7a8329ed79836d709")
    version("0.12", sha256="39e7c9f8644d1af310d076c1a5cc648040033e4724e7edfd85eb983ad88336d0")

    depends_on("c", type="build")  # generated
