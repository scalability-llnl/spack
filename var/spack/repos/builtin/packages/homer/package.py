# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class Homer(Package):
    """Software for motif discovery and next generation sequencing analysis"""

    homepage = "http://homer.ucsd.edu/homer"
    url = "http://homer.ucsd.edu/homer/data/software/homer.v4.9.1.zip"

    license("GPL-3.0-only")

    version("4.11.1", sha256="80d1cd00616729894017b24a36a2ef81f9cde8bd364e875aead1e0cfb500c82b")
    version("4.9.1", sha256="ad1303b0b0400dc8a88dbeae1ee03a94631977b751a3d335326c4febf0eec3a9")

    depends_on("perl", type=("build", "run"))
    depends_on("r-biocgenerics", type="run")
    depends_on("r-biocparallel", type="run")
    depends_on("r-edger", type="run")
    depends_on("r-deseq2", type="run")

    variant("data", default=False, description="Download genome data packages")

    def install(self, spec, prefix):
        # initialize homer directories
        basedir = join_path(prefix.lib, "homer")
        mkdirp(basedir)

        install_tree(".", basedir)

        # symlink bin so it is included in the PATH
        symlink(join_path(basedir, "bin"), prefix.bin)

        # override homer base directory in configure script
        filter_file(
            "my $homeDir = $1;",
            'my $homeDir = "{0}";'.format(basedir),
            "configureHomer.pl",
            string=True,
        )

        # compile/prepare binaries and perl scripts with the correct paths
        perl = which("perl")
        perl("configureHomer.pl", "-local")

        # download extra data if requested
        if spec.satisfies("+data"):
            perl("configureHomer.pl", "-install", "-all")
