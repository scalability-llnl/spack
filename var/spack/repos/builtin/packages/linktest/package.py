# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Linktest(MakefilePackage):
    """Performance tool to generate communication matrix using
    parallel ping-pong benchmark"""

    homepage = (
        "https://www.fz-juelich.de/ias/jsc/EN/Expertise/Support/Software/LinkTest/_node.html"
    )
    url = "https://apps.fz-juelich.de/jsc/linktest/download.php?version=1.2p1"

    maintainers("pramodk")

    version(
        "1.2p1",
        sha256="981b96da1d5bf214507b8e219a36e8d0183d8bd5c10539b26f660b2c83e5269d",
        extension="tar.gz",
    )

    depends_on("c", type="build")  # generated

    depends_on("mpi")
    depends_on("sionlib")

    def edit(self, spec, prefix):
        with working_dir("src"):
            makefile = FileFilter("Makefile")
            makefile.filter("= gcc", "= cc")
            makefile.filter("mpicc", spec["mpi"].mpicc)
            makefile.filter("#SIONLIB_INST=.*", "SIONLIB_INST=%s" % spec["sionlib"].prefix)

    def build(self, spec, prefix):
        with working_dir("src"):
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("src/mpilinktest", prefix.bin)
        install("src/pingponganalysis", prefix.bin)
