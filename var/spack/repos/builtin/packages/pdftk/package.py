# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Pdftk(MakefilePackage):
    """PDFtk Server is a command-line tool for working with PDFs. It is
    commonly used for client-side scripting or server-side processing
    of PDFs."""

    homepage = "https://www.pdflabs.com/tools/pdftk-server"
    url = "https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk-2.02-src.zip"
    # Alternative download locations:
    # https://sources.debian.org/src/pdftk/
    # http://archive.ubuntu.com/ubuntu/pool/universe/p/pdftk/pdftk_2.02.orig.tar.gz

    maintainers("citibeth")

    version("2.02", sha256="118f6a25fd3acaafb58824dce6f97cdc07e56050e666b90e4c4ef426ea37b8c1")

    depends_on("eclipse-gcj-parser", type="build")

    # Only takes effect in phases not overridden here
    build_directory = "pdftk"

    # https://www.pdflabs.com/docs/install-pdftk-on-redhat-or-centos/
    def edit(self, spec, prefix):
        # ------ Fix install directory in main Makefile
        makefile = FileFilter(join_path("pdftk", "Makefile.Base"))
        makefile.filter("/usr/local/bin", spec.prefix.bin)

        # ------ Create new config file
        compiler = self.compiler
        gcc_base = os.path.split(os.path.split(compiler.cxx)[0])[0]
        gcc_version = compiler.version

        cppflags = (
            "-DPATH_DELIM=0x2f",
            "-DASK_ABOUT_WARNINGS=false",
            "-DUNBLOCK_SIGNALS",
            "-fdollars-in-identifiers",
        )
        cxxflags = ("-Wall", "-Wextra", "-Weffc++", "-O2")
        gcjflags = ("-Wall", "-Wextra", "-O2")
        vars = [
            ("VERSUFF", "-%s" % gcc_version),
            ("CXX", compiler.cxx),
            ("GCJ", spec["eclipse-gcj-parser"].package.gcj),
            ("GCJH", join_path(gcc_base, "bin", "gcjh")),
            ("GJAR", join_path(gcc_base, "bin", "gjar")),
            ("LIBGCJ", join_path(gcc_base, "share", "java", "libgcj-{0}.jar".format(gcc_version))),
            ("AR", "ar"),
            ("RM", "rm"),
            ("ARFLAGS", "rs"),
            ("RMFLAGS", "-vf"),
            ("CPPFLAGS", " ".join(cppflags)),
            ("CXXFLAGS", " ".join(cxxflags)),
            ("GCJFLAGS", " ".join(gcjflags)),
            ("GCJHFLAGS", "-force"),
            ("LDLIBS", "-lgcj"),
        ]
        with open(join_path("pdftk", "Makefile.Spack"), "w") as mk:
            for var, val in vars:
                mk.write("export {0}={1}\n".format(var, str(val)))
            mk.write("include Makefile.Base\n")

    def build(self, spec, prefix):
        compiler = self.compiler
        gcc_base = os.path.split(os.path.split(compiler.cxx)[0])[0]
        env["PATH"] = join_path(gcc_base, "bin") + ":" + env["PATH"]
        with working_dir(self.build_directory):
            make("-f", "Makefile.Spack", parallel=False)

    def install(self, spec, prefix):
        mkdirp(self.spec.prefix.bin)
        with working_dir(self.build_directory):
            make("-f", "Makefile.Spack", "install", parallel=False)
