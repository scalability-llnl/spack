# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Debugedit(AutotoolsPackage):
    """
    Debugedit is a set of libraries and programs for creating and editing
    debuginfo. It allows you to get build-ids and rewrite DWARF source paths.
    Debugedit was originally part of the rpm project, and now exists
    as its own separate project and is maintained by RedHat.
    """

    homepage = "https://www.sourceware.org/debugedit/"
    git = "git://sourceware.org/git/debugedit.git"
    url = "https://sourceware.org/ftp/debugedit/0.2/debugedit-0.2.tar.xz"

    license("LGPL-2.1-or-later")

    version("develop", branch="main")
    version("0.2", sha256="b78258240bb7ec5bbff109495092dcc111aa0393f135f2d2a4b43887ba26a942")

    depends_on("c", type="build")  # generated

    depends_on("help2man", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("elfutils")  # requires libdw
    depends_on("libiberty")

    def build(self, spec, prefix):
        # requires libiberty
        libiberty = spec["libiberty"].prefix.include.libiberty
        make("CPPFLAGS=-I%s" % libiberty)
