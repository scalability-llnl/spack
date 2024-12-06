# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Babeltrace(AutotoolsPackage):
    """Babeltrace is a trace viewer and converter reading and writing the
    Common Trace Format (CTF). Its main use is to pretty-print CTF traces
    into a human-readable text output ordered by time."""

    homepage = "https://www.efficios.com/babeltrace"
    url = "https://www.efficios.com/files/babeltrace/babeltrace-1.2.4.tar.bz2"

    license("MIT")

    version("1.5.11", sha256="67b43aaaef5c951fa7af1a557cf7201a11fe89876b7c22ba0a03cbc316db5a9c")
    version("1.2.4", sha256="666e3a1ad2dc7d5703059963056e7800f0eab59c8eeb6be2efe4f3acc5209eb1")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("glib@2.22:", type=("build", "link"))
    depends_on("uuid")
    depends_on("popt")
