# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cqrlib(MakefilePackage):
    """CQRlib -- ANSI C API for Quaternion Rotations"""

    homepage = "https://cqrlib.sourceforge.net/"

    license("LGPL-2.1-or-later")

    version("1.1.3", sha256="90ecd9aabfb72e55e56957c7b233910d18b8c2bb522a8e59eddbcc4618c72d0e")
    version("1.1.2", sha256="af3cf2402974579f3c6efc6a6174a5da52786db4bfee9d38d504d93bc42410fd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libtool", type="build")

    patch("cqr.patch", when="@1.1.2")
    patch("Makefile.patch", when="@1.1.2:")

    def url_for_version(self, version):
        full_vers = str(version)
        return f"https://downloads.sourceforge.net/project/cqrlib/cqrlib/CQRlib-{full_vers}/CQRlib-{full_vers}.tar.gz"

    def edit(self, spec, prefix):
        mf = FileFilter("Makefile")
        mf.filter(r"^CC.+", "CC = {0}".format(spack_cc))
        mf.filter(r"^CXX.+", "CXX = {0}".format(spack_cxx))
        mf.filter(r"^INSTALLDIR .+", "INSTALLDIR = {0}".format(prefix))

    def build(self, spec, prefix):
        pass
