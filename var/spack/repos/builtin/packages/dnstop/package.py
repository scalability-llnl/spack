# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dnstop(AutotoolsPackage):
    """Stay on top of your DNS traffic."""

    homepage = "https://github.com/measurement-factory/dnstop"
    git = "https://github.com/measurement-factory/dnstop.git"

    license("BSD-3-Clause")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    depends_on("libpcap")
    depends_on("ncurses")

    def configure_args(self):
        return ["LIBS=-ltinfo"]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.share.man.man8)
        make("BINPATH={0}".format(prefix.bin), "MANPATH={0}/".format(prefix), "install")
