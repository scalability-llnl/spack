# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spades(CMakePackage):
    """SPAdes - St. Petersburg genome assembler - is intended for both
    standard isolates and single-cell MDA bacteria assemblies."""

    homepage = "https://cab.spbu.ru/software/spades/"
    url = "https://github.com/ablab/spades/releases/download/v3.15.3/SPAdes-3.15.3.tar.gz"
    maintainers("snehring")

    version("4.0.0", sha256="07c02eb1d9d90f611ac73bdd30ddc242ed51b00c8a3757189e8a8137ad8cfb8b")
    version("3.15.5", sha256="155c3640d571f2e7b19a05031d1fd0d19bd82df785d38870fb93bd241b12bbfa")
    version("3.15.3", sha256="b2e5a9fd7a65aee5ab886222d6af4f7b7bc7f755da7a03941571fabd6b9e1499")
    version("3.15.0", sha256="6719489fa4bed6dd96d78bdd4001a30806d5469170289085836711d1ffb8b28b")
    version("3.14.1", sha256="d629b78f7e74c82534ac20f5b3c2eb367f245e6840a67b9ef6a76f6fac5323ca")
    version("3.13.0", sha256="c63442248c4c712603979fa70503c2bff82354f005acda2abc42dd5598427040")
    version("3.12.0", sha256="15b48a3bcbbe6a8ad58fd04ba5d3f1015990fbfd9bdf4913042803b171853ac7")
    version("3.11.1", sha256="3ab85d86bf7d595bd8adf11c971f5d258bbbd2574b7c1703b16d6639a725b474")
    version("3.10.1", sha256="d49dd9eb947767a14a9896072a1bce107fb8bf39ed64133a9e2f24fb1f240d96")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python", type=("build", "run"))
    depends_on("zlib-api")
    depends_on("bzip2")

    variant("sra", default=True, description="Build with ncbi sra file support", when="@4:")
    variant("tools", default=True, description="Build additional tools", when="@4:")

    # SPAdes will explicitly not compile with gcc < 5.3.0
    conflicts("%gcc@:5.2.9")

    conflicts("%gcc@7.1.0:", when="@:3.10.1")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        args = [self.define_from_variant("SPADES_USE_NCBISDK", "sra")]
        if self.spec.satisfies("+tools"):
            args.append("-DSPADES_ENABLE_PROJECTS:STRING=all")
        return args
