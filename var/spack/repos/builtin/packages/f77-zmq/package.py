# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class F77Zmq(MakefilePackage):
    """Fortran binding for the ZeroMQ communication library"""

    homepage = "https://zguide.zeromq.org/"
    url = "https://github.com/zeromq/f77_zmq/archive/4.3.1.tar.gz"

    maintainers("scemama")

    license("LGPL-2.1-or-later")

    version("4.3.2", sha256="f1fb7544d38d9bb7235f98c96f241875ddcb0d37ed950618c23d4e4d666a73ca")
    version("4.3.1", sha256="a15d72d93022d3e095528d2808c7767cece974a2dc0e2dd95e4c122f60fcf0a8")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("libzmq")
    depends_on("python@3:", type="build", when="@:4.3.1")
    depends_on("python", type="build", when="@4.3.2:")

    def setup_build_environment(self, env):
        env.append_flags("CFLAGS", "-O3")
        env.append_flags("CFLAGS", "-g")

    def edit(self, spec, prefix):
        cflags = os.environ.get("CFLAGS")
        makefile = FileFilter("Makefile")
        makefile.filter("CC=.*", "CC={0} {1}".format(spack_cc, self.compiler.cc_pic_flag))
        makefile.filter("CFLAGS=.*", "CFLAGS={0}".format(cflags))
        makefile.filter("PREFIX=.*", "PREFIX={0}".format(self.prefix))
        p = self.spec["libzmq"].prefix
        os.environ["ZMQ_H"] = "{0}/include/zmq.h".format(p)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)
