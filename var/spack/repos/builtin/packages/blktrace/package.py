# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blktrace(MakefilePackage):
    """
    blktrace is a block layer IO tracing mechanism which provides detailed
    information about request queue operations up to user space. There are
    three major components: a kernel component, a utility to record the i/o
    trace information for the kernel to user space, and utilities to analyse
    and view the trace information.
    """

    homepage = "https://brick.kernel.dk"
    url = "https://brick.kernel.dk/snaps/blktrace-1.2.0.tar.gz"

    license("GPL-2.0-only")

    version("1.3.0", sha256="88c25b3bb3254ab029d4c62df5a9ab863a5c70918a604040da8fe39873c6bacb")
    version("1.2.0", sha256="d14029bc096026dacb206bf115c912dcdb795320b5aba6dff3e46d7f94c5242d")
    version("1.1.0", sha256="dc1e5da64b8fef454ec24aa4fcc760112b4ea7c973e2485961aa5668b3a8ce1d")
    version("1.0.5", sha256="783b4c8743498de74b3492725815d31f3842828baf8710c53bc4e7e82cee387c")
    version("1.0.4", sha256="c1b53e2382f7309e822d48fef187cf44e84bb44df52a0a9786d447d127af75cf")
    version("1.0.3", sha256="78c6825212fe6700039fab77d53bc02e6b324e712caea718fff190e4e034cfa8")
    version("1.0.2", sha256="15f01e2a952919ba3c7b90f8bd891d1a98c454626501094030df632666786343")

    depends_on("c", type="build")  # generated

    depends_on("libaio")

    def edit(self, spec, prefix):
        makefiles = ["Makefile", "btreplay/Makefile", "btt/Makefile", "iowatcher/Makefile"]
        for m in makefiles:
            makefile = FileFilter(m)
            makefile.filter("CC.*=.*", "CC = {0}".format(spack_cc))

    def install(self, spec, prefix):
        install_tree(".", prefix)
