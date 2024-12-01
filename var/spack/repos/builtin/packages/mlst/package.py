# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mlst(Package):
    """Scan contig files against traditional PubMLST typing schemes"""

    homepage = "https://github.com/tseemann/mlst"
    url = "https://github.com/tseemann/mlst/archive/refs/tags/v2.22.1.tar.gz"

    license("GPL-2.0-only")

    version("2.23.0", sha256="35bdbde309ba25293c3cce417d82e79594b9f78365133062923dc3d629bd8846")
    version("2.22.1", sha256="a8f64d7cb961a8e422e96a19309ad8707f8792d9f755a9e5a1f5742986d19bca")

    depends_on("perl@5.26:", type="run")
    depends_on("perl-moo", type="run")
    depends_on("perl-list-moreutils", type="run")
    depends_on("perl-json", type="run")
    depends_on("perl-file-which", type="run")
    depends_on("blast-plus@2.9.0:", type="run")
    depends_on("any2fasta", type="run")
    # dependencies for scripts
    depends_on("parallel", type="run")
    depends_on("curl", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.db)
        mkdirp(prefix.perl5)
        install_tree("bin", prefix.bin)
        install_tree("scripts", prefix.bin)
        install_tree("db", prefix.db)
        install_tree("perl5", prefix.perl5)
