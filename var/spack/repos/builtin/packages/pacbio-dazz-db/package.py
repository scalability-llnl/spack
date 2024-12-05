# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PacbioDazzDb(MakefilePackage):
    """The Dazzler Database Library. This version is a special fork
    required for some pacbio utilities."""

    homepage = "https://github.com/PacificBiosciences/DAZZ_DB"
    git = "https://github.com/PacificBiosciences/DAZZ_DB.git"

    version("2017-04-10", commit="f29d27d51f460563481cd227d17f4bdc5e288365")

    depends_on("c", type="build")  # generated

    depends_on("gmake", type="build")

    def edit(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        makefile = FileFilter("Makefile")
        makefile.filter(r"DEST_DIR\s*=\s*~/bin", "DEST_DIR = " + prefix.bin)
        gmf = FileFilter("GNUmakefile")
        gmf.filter(r"rsync\s*-av\s*\$\{ALL\}\s*\$\{PREFIX\}/bin", "cp ${ALL} " + prefix.bin)
        gmf.filter(r"rsync\s*-av\s*libdazzdb.*\s*\$\{PREFIX\}/lib", "cp libdazzdb.* " + prefix.lib)
        gmf.filter(
            (r"rsync\s*-av\s*\$\(wildcard\s*\$\{THISDIR\}/\*.h" r"\)\s*\$\{PREFIX\}/include"),
            "cp *.h " + prefix.include,
        )
