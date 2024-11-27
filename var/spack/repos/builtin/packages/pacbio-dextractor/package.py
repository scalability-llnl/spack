# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PacbioDextractor(MakefilePackage):
    """The Dextractor and Compression Command Library. This is a special
    fork required by some pacbio utilities."""

    homepage = "https://github.com/PacificBiosciences/DEXTRACTOR"
    git = "https://github.com/PacificBiosciences/DEXTRACTOR.git"

    version("2016-08-09", commit="89726800346d0bed15d98dcc577f4c7733aab4b1")

    depends_on("c", type="build")  # generated

    depends_on("hdf5")
    depends_on("gmake", type="build")

    def edit(self, spec, prefix):
        mkdirp(prefix.bin)
        makefile = FileFilter("Makefile")
        makefile.filter(
            r"PATH_HDF5\s*=\s*/sw/apps/hdf5/current", "PATH_HDF5 = " + spec["hdf5"].prefix
        )
        makefile.filter(r"PATH_HDF5\*s=\s*/usr/local/hdf5", "")
        makefile.filter(r"DEST_DIR\s*=\s*~/bin", "DEST_DIR = " + prefix.bin)
        gmf = FileFilter("GNUmakefile")
        gmf.filter(r"rsync\s*-av\s*\$\{ALL\}\s*\$\{PREFIX\}/bin", "cp ${ALL} " + prefix.bin)
