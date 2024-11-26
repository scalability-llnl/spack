# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class BlastLegacy(Package):
    """Legacy NCBI BLAST distribution -- no longer supported.
    Contains older programs including `blastall'"""

    homepage = "https://www.ncbi.nlm.nih.gov/"
    url = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/ncbi.tar.gz"

    version(
        "2.2.26",
        sha256="d8fffac25efc8ca894c707c840a4797a8a949ae6fd983d2f91c9972f788efb7d",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("tcsh", type="build")

    def install(self, spec, prefix):
        filter_file("/bin/csh -f", "/usr/bin/env tcsh", "make/ln-if-absent", string=True)

        symlink(self.stage.source_path, "../ncbi")
        tcsh = which("tcsh")
        with working_dir(".."):
            tcsh("./ncbi/make/makedis.csh")

        # depends on local data in the source tree
        install_path = join_path(prefix, "usr/local/blast-legacy")
        mkdirp(install_path)
        install_tree(".", install_path)

        # symlink build output with binaries
        symlink(join_path(install_path, "build"), prefix.bin)
