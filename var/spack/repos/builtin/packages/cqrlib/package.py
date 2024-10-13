# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cqrlib(MakefilePackage):
    """CQRlib -- ANSI C API for Quaternion Rotations"""

    homepage = "https://cqrlib.sourceforge.net/"
    url = (
        "https://downloads.sourceforge.net/project/cqrlib/cqrlib/CQRlib-1.1.2/CQRlib-1.1.2.tar.gz"
    )

    license("LGPL-2.1-or-later")

    version("1.1.2", sha256="af3cf2402974579f3c6efc6a6174a5da52786db4bfee9d38d504d93bc42410fd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libtool", type="build")

    patch("cqr.patch")

    def edit(self, spec, prefix):
        mf = FileFilter("Makefile")
        mf.filter(r"^CC.+", "CC = {0}".format(spack_cc))
        mf.filter(r"^CXX.+", "CXX = {0}".format(spack_cxx))
        mf.filter(r"^INSTALLDIR .+", "INSTALLDIR = {0}".format(prefix))

    def build(self, spec, prefix):
        pass
