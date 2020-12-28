# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Argobots(AutotoolsPackage):
    """Argobots, which was developed as a part of the Argo project, is
    a lightweight runtime system that supports integrated computation
    and data movement with massive concurrency. It will directly
    leverage the lowest-level constructs in the hardware and OS:
    lightweight notification mechanisms, data movement engines, memory
    mapping, and data placement strategies. It consists of an
    execution model and a memory model."""

    homepage = "http://www.argobots.org/"
    url      = "https://github.com/pmodels/argobots/releases/download/v1.0b1/argobots-1.0b1.tar.gz"
    git      = "https://github.com/pmodels/argobots.git"
    maintainers = ['shintaro-iwasaki']

    version("main", branch="main")
    version("1.0", sha256="36a0815f7bf99900a9c9c1eef61ef9b3b76aa2cfc4594a304f6c8c3296da8def")

    variant("valgrind", default=False, description="Enable Valgrind")
    variant("debug", default=False, description="Compiled with debugging symbols")

    depends_on("m4", type=("build"), when="@main")
    depends_on("autoconf", type=("build"), when="@main")
    depends_on("automake", type=("build"), when="@main")
    depends_on("libtool", type=("build"), when="@main")
    depends_on("valgrind", when="+valgrind")

    def configure_args(self):
        args = ["--enable-perf-opt"]
        if '+valgrind' in self.spec:
            args.append('--enable-valgrind')
        else:
            args.append('--disable-valgrind')

        if '+debug' in self.spec:
            args.append('--enable-debug=yes')
        else:
            args.append('--disable-debug')

        return args
