# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class P7zip(MakefilePackage):
    """A Unix port of the 7z file archiver"""

    maintainers("vmiheer")
    homepage = "https://p7zip.sourceforge.net"

    license("DOC")

    version("17.05", sha256="d2788f892571058c08d27095c22154579dfefb807ebe357d145ab2ddddefb1a6")
    version("17.04", sha256="ea029a2e21d2d6ad0a156f6679bd66836204aa78148a4c5e498fe682e77127ef")
    version("16.02", sha256="5eb20ac0e2944f6cb9c2d51dd6c4518941c185347d4089ea89087ffdd6e2341f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch(
        "gcc10.patch",
        when="@16.02%gcc@10:",
        sha256="96914025b9f431fdd75ae69768162d57751413634622f9df1a4bc4960e7e8fe1",
    )

    # Replace boolean increments with assignments of true (which is
    # semantically equivalent). Use of increment operators on booleans is
    # forbidden by C++17, the default standard targeted by GCC 11.
    patch(
        "gcc11.patch",
        when="@16.02%gcc@11:",
        sha256="39dd15f2dfc86eeee8c3a13ffde65c2ca919433cfe97ea126fbdc016afc587d1",
    )

    # all3 includes 7z, 7za, and 7zr
    build_targets = ["all3"]

    depends_on("yasm", type="build", when="%clang")

    # Old package is abandoned, newer versions come from a fork
    def url_for_version(self, version):
        if version >= Version("17"):
            return "https://github.com/p7zip-project/p7zip/archive/refs/tags/v{0}.tar.gz".format(
                version
            )
        else:
            return "https://downloads.sourceforge.net/project/p7zip/p7zip/{0}/p7zip_{0}_src_all.tar.bz2".format(
                version
            )

    def edit(self, spec, prefix):
        # Use the suggested makefile
        for tgt, makefile in {
            "platform=linux %clang": "makefile.linux_clang_amd64_asm",
            "platform=darwin %gcc": "makefile.macosx_gcc_64bits",
            "platform=darwin %apple-clang": "makefile.macosx_llvm_64bits",
            "platform=darwin %clang": "makefile.macosx_llvm_64bits",
        }.items():
            if tgt in self.spec:
                copy(makefile, "makefile.machine")
                break
        # Silence an error about -Wc++11-narrowing in clang.
        if "@16.02 %clang" in spec:
            with open("makefile.machine", "a") as f:
                f.write("ALLFLAGS += -Wno-c++11-narrowing")

    @property
    def install_targets(self):
        return ["DEST_HOME={0}".format(self.prefix), "install"]
