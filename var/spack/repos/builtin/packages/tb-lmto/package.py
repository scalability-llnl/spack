# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class TbLmto(MakefilePackage):
    """
    The STUTTGART TB-LMTO program. The linear muffin-tin orbital (LMTO) method has been described in numerous publications.
    Use of this software is subject to the license at
    https://www2.fkf.mpg.de/andersen/LMTODOC/node180.html#SECTION000130000000000000000
    """

    homepage = "https://www2.fkf.mpg.de/andersen/LMTODOC/LMTODOC.html"
    manual_download = True

    maintainers("snehring")

    version(
        "20240601-47.1d", sha256="5b24f2917cef85fe49d3a4ff6403294a44a9cf7c003234a0fd96d626c316bda0"
    )
    version(
        "20240601-47c2.1d",
        sha256="c80ef9b4aa725ad75ae07b0215671b3674a8f5dced9e87202dd0d486ffe1cb10",
    )
    version(
        "20240601-47u.1d",
        sha256="bbcc1c57005f33749f8ee6d33be3490071704bce11214544cc4f9c13c28a126e",
    )

    depends_on("c", type="build")
    depends_on("fortran", type="build")
    depends_on("gnuplot", type="run")

    parallel = False

    @property
    def build_targets(self):
        # something about the spack wrapper breaks this, it's extremely weird
        return [
            f"CC={self.compiler.cc}",
            f"FC={self.compiler.fc} -finit-local-zero -fallow-argument-mismatch",
            "all",
        ]

    def url_for_version(self, version):
        return f"file://{os.getcwd()}/lmto{version.string.split('-')[1]}.tar.gz"

    def edit(self, spec, prefix):
        makefile = FileFilter("makefile")
        makefile.filter("LMPATH = .*", "LMPATH = ./")
        makefile.filter("^FFLAGS =.*", "")
        makefile.filter("^CCFLAGS =.*", "")
        makefile.filter("CC=.*", "")
        makefile.filter("FC=.*", "")

    def install(self, spec, prefix):
        mkdirp(prefix)
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
