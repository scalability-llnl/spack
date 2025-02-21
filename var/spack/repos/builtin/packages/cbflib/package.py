# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cbflib(MakefilePackage):
    """CBFLIB is a library of ANSI-C functions providing a simple mechanism
    for accessing Crystallographic Binary Files (CBF files) and
    Image-supporting CIF (imgCIF) files."""

    homepage = "http://www.bernstein-plus-sons.com/software/CBF/"
    url = (
        "https://downloads.sourceforge.net/project/cbflib/cbflib/CBFlib_0.9.2/CBFlib-0.9.2.tar.gz"
    )

    license("Unlicense")

    version("0.9.2", sha256="367e37e1908a65d5472e921150291332823a751206804866e752b793bca17afc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("m4", type="build")

    patch("cbf_f16.patch")
    patch("cbf_int.patch")

    def setup_build_environment(self, env):
        ce = Executable(self.compiler.cc)
        ce(
            "-E",
            join_path(os.path.dirname(__file__), "checkint.c"),
            output=str,
            error=str,
            fail_on_error=False,
        )
        if ce.returncode != 0:
            env.set("CBF_DONT_USE_LONG_LONG", "1")

    def edit(self, spec, prefix):
        mf = FileFilter("Makefile")
        mf.filter(r"^CC.+", "CC = {0}".format(spack_cc))
        mf.filter(r"^C\+\+.+", "C++ = {0}".format(spack_cxx))
        mf.filter("gfortran", spack_fc)
        mf.filter(r"^INSTALLDIR .+", "INSTALLDIR = {0}".format(prefix))
        if self.spec.satisfies("%gcc@10:"):
            mf.filter(r"^F90FLAGS[ \t]*=[ \t]*(.+)", "F90FLAGS = \\1 -fallow-invalid-boz")

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        make("install", parallel=False)
