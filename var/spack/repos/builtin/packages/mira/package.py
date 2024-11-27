# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Mira(AutotoolsPackage):
    """MIRA is a multi-pass DNA sequence data assembler/mapper for whole genome
    and EST/RNASeq projects."""

    homepage = "https://sourceforge.net/projects/mira-assembler/"
    url = "https://downloads.sourceforge.net/project/mira-assembler/MIRA/stable/mira-4.0.2.tar.bz2"

    license("GPL-2.0-or-later")

    version("4.0.2", sha256="a32cb2b21e0968a5536446287c895fe9e03d11d78957554e355c1080b7b92a80")

    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.46:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("expat@2.0.1:")
    depends_on("gperftools")

    conflicts("%gcc@6:", when="@:4.0.2")

    def patch(self):
        with working_dir(join_path("src", "progs")):
            edit = FileFilter("quirks.C")
            edit.filter(
                "#include <boost/filesystem.hpp>",
                "#include <boost/filesystem.hpp>\n#include <iostream>",
            )

    def configure_args(self):
        args = [
            "--with-boost=%s" % self.spec["boost"].prefix,
            "--with-expat=%s" % self.spec["expat"].prefix,
        ]
        return args
