# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Repeatmodeler(Package):
    """RepeatModeler is a de-novo repeat family identification and modeling
    package."""

    homepage = "https://www.repeatmasker.org/RepeatModeler/"
    url = "https://github.com/Dfam-consortium/RepeatModeler/archive/refs/tags/2.0.4.tar.gz"

    maintainers("snehring")

    license("OSL-2.1")

    version("2.0.4", sha256="94aad46cc70911d48de3001836fc3165adb95b2b282b5c53ab0d1da98c27a6b6")
    version(
        "1.0.11",
        sha256="7ff0d588b40f9ad5ce78876f3ab8d2332a20f5128f6357413f741bb7fa172193",
        url="https://www.repeatmasker.org/RepeatModeler/RepeatModeler-open-1.0.11.tar.gz",
    )

    depends_on("perl", type=("build", "run"))
    depends_on("perl-json", type=("build", "run"))
    depends_on("perl-uri", type=("build", "run"))
    depends_on("perl-libwww-perl", type=("build", "run"))
    depends_on("perl-file-which", type=("build", "run"), when="@2.0.4:")
    depends_on("perl-devel-size", type=("build", "run"), when="@2.0.4:")

    depends_on("repeatmasker", type="run")
    depends_on("recon+repeatmasker", type="run")
    depends_on("repeatscout", type="run")
    depends_on("trf", type="run")
    depends_on("nseg", type="run")
    depends_on("ncbi-rmblastn", type="run")

    # "optional" dependencies that it still wants
    depends_on("cdhit", type="run", when="@2.0.4:")
    depends_on("genometools", type="run", when="@2.0.4:")
    depends_on("mafft", type="run", when="@2.0.4:")
    depends_on("ninja-phylogeny", type="run", when="@2.0.4:")
    depends_on("blat", type="run", when="@2.0.4:")
    depends_on("ltr-retriever", type="run", when="@2.0.4:")

    def install(self, spec, prefix):
        # interactive configuration script
        if spec.satisfies("@1.0.11"):
            config_answers = [
                "",
                "",
                "",
                spec["repeatmasker"].prefix.bin,
                spec["recon"].prefix.bin,
                spec["repeatscout"].prefix.bin,
                spec["nseg"].prefix.bin,
                spec["trf"].prefix.bin,
                "1",
                spec["ncbi-rmblastn"].prefix.bin,
                "Y",
                "3",
            ]
        elif spec.satisfies("@2.0.4:"):
            config_answers = [
                "",
                spec["repeatmasker"].prefix.bin,
                spec["recon"].prefix.bin,
                spec["repeatscout"].prefix.bin,
                spec["trf"].prefix.bin,
                spec["cdhit"].prefix.bin,
                spec["blat"].prefix.bin,
                spec["ncbi-rmblastn"].prefix.bin,
                "y",
                spec["genometools"].prefix.bin,
                spec["ltr-retriever"].prefix.bin,
                spec["mafft"].prefix.bin,
                spec["ninja-phylogeny"].prefix.bin,
            ]

        config_filename = "spack-config.in"

        with open(config_filename, "w") as f:
            f.write("\n".join(config_answers))

        with open(config_filename, "r") as f:
            perl = which("perl")
            perl("configure", input=f)

        install_tree(".", prefix.bin)
