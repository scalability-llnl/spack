# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bannergrab(MakefilePackage):
    """Bannergrab is a simple tool, designed to collect information
    from network services. It can do this using two different methods;
    grab the connection banners and send triggers and collect the
    responses. Bannergrab defaults to sending triggers."""

    homepage = "https://github.com/johanburati/bannergrab"
    git = "https://github.com/johanburati/bannergrab.git"

    license("GPL-3.0-or-later")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man1)
        make("BINPATH={0}".format(prefix.bin), "MANPATH={0}/".format(prefix), "install")
