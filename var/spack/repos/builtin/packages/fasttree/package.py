# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class Fasttree(Package):
    """FastTree infers approximately-maximum-likelihood phylogenetic
    trees from alignments of nucleotide or protein sequences.
    """

    homepage = "http://www.microbesonline.org/fasttree"
    url = "http://www.microbesonline.org/fasttree/FastTree-2.1.10.c"
    maintainers("snehring")

    version(
        "2.1.11",
        sha256="9026ae550307374be92913d3098f8d44187d30bea07902b9dcbfb123eaa2050f",
        expand=False,
        url="http://www.microbesonline.org/fasttree/FastTree-2.1.11.c",
    )
    version(
        "2.1.10",
        sha256="54cb89fc1728a974a59eae7a7ee6309cdd3cddda9a4c55b700a71219fc6e926d",
        expand=False,
        url="http://www.microbesonline.org/fasttree/FastTree-2.1.10.c",
    )

    variant("openmp", default=True, description="Add openmp support to Fasttree.")

    def install(self, spec, prefix):
        cc = Executable(spack_cc)
        if self.spec.satisfies("+openmp"):
            cc(
                "-O3",
                self.compiler.openmp_flag,
                "-DOPENMP",
                "-finline-functions",
                "-funroll-loops",
                "-Wall",
                "-oFastTree",
                "FastTree-" + format(spec.version.dotted) + ".c",
                "-lm",
            )
        else:
            cc(
                "-O3",
                "-finline-functions",
                "-funroll-loops",
                "-Wall",
                "-oFastTree",
                "FastTree-" + format(spec.version.dotted) + ".c",
                "-lm",
            )

        mkdir(prefix.bin)
        install("FastTree", prefix.bin)

    @run_after("install")
    def create_fasttree_mp_symlink(self):
        with working_dir(prefix.bin):
            if self.spec.satisfies("+openmp"):
                symlink("FastTree", "FastTreeMP")
