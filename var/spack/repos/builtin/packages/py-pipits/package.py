# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPipits(PythonPackage):
    """Automated pipeline for analyses of fungal ITS from the Illumina"""

    homepage = "https://github.com/hsgweon/pipits"
    url = "https://github.com/hsgweon/pipits/archive/2.4.tar.gz"

    version("2.4", sha256="b08a9d70ac6e5dd1c64d56b77384afd69e21e7d641b2fc4416feff862a2cd054")

    # https://github.com/bioconda/bioconda-recipes/blob/master/recipes/pipits/meta.yaml
    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pispino@1.1:", type=("build", "run"))
    depends_on("vsearch", type="run")
    depends_on("fastx-toolkit", type="run")
    depends_on("hmmer", type="run")
    depends_on("itsx", type="run")
    depends_on("py-biom-format", type=("build", "run"))
    depends_on("rdptools", type="run")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-progressbar2", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("seqkit", type="run")

    resource(
        name="UNITE_retrained",
        url="http://sourceforge.net/projects/pipits/files/UNITE_retrained_28.06.2017.tar.gz",
        destination="refdb",
    )

    resource(
        name="uchime_reference_dataset_01.01.2016.fasta",
        url="https://unite.ut.ee/sh_files/uchime_reference_dataset_01.01.2016.zip",
        destination=join_path("refdb", "uchime_reference_dataset_01.01.2016"),
    )

    resource(
        name="warcup_retrained_V2",
        url="https://sourceforge.net/projects/pipits/files/warcup_retrained_V2.tar.gz",
        destination="refdb",
    )

    @run_after("install")
    def install_db(self):
        install_tree(join_path(self.stage.source_path, "refdb"), self.prefix.refdb)

    def setup_run_environment(self, env):
        env.set(
            "PIPITS_UNITE_REFERENCE_DATA_CHIMERA",
            join_path(
                self.prefix,
                "refdb",
                "uchime_reference_dataset_01.01.2016",
                "uchime_reference_dataset_01.01.2016.fasta",
            ),
        )
        env.set("PIPITS_UNITE_RETRAINED_DIR", self.prefix.refdb.UNITE_retrained)
        env.set("PIPITS_WARCUP_RETRAINED_DIR", self.prefix.refdb.warcup_retrained_V2)
        env.set(
            "PIPITS_RDP_CLASSIFIER_JAR",
            join_path(self.spec["rdp-classifier"].prefix.bin, "classifier.jar"),
        )
