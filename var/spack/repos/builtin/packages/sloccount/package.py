# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sloccount(MakefilePackage):
    """SLOCCount is a set of tools for counting physical Source Lines of Code
    (SLOC) in a large number of languages of a potentially large set of
    programs."""

    homepage = "https://dwheeler.com/sloccount/"
    url = "https://dwheeler.com/sloccount/sloccount-2.26.tar.gz"

    license("GPL-2.0-or-later")

    version("2.26", sha256="fa7fa2bbf2f627dd2d0fdb958bd8ec4527231254c120a8b4322405d8a4e3d12b")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # md5sum needed at run-time
    depends_on("coreutils", type=("build", "run"))
    depends_on("flex", type="build")

    def edit(self, spec, prefix):
        makefile = FileFilter("makefile")
        makefile.filter("^PREFIX=.*", "PREFIX=" + prefix)
        makefile.filter("^CC=.*", "CC=" + spack_cc)

        # Needed for `make test` to pass
        makefile.filter("PATH=.:${PATH}", "PATH=$(CURDIR):${PATH}", string=True)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        make("install")
