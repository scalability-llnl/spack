# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pcma(MakefilePackage):
    """PCMA is a progressive multiple sequence alignment program that combines
    two different alignment strategies."""

    homepage = "http://prodata.swmed.edu/pcma/pcma.php"
    url = "http://prodata.swmed.edu/download/pub/PCMA/pcma.tar.gz"

    version("2.0", sha256="4b92d412126d393baa3ede501cafe9606ada9a66af6217d56befd6ec2e0c01ba")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        makefile = FileFilter("makefile")
        makefile.filter("gcc", spack_cc)
        if spec.satisfies("%gcc@10:"):
            # they missed one
            filter_file(r"^sint \*seqlen_array;$", "extern sint *seqlen_array;", "calctree.c")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("pcma", prefix.bin)

    # set return value and change return type of function [-Wreturn-type]
    patch("fix_return_type_err.patch")
