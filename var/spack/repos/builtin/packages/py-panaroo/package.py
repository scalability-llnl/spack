# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPanaroo(PythonPackage):
    """A Bacterial Pangenome Analysis Pipeline"""

    homepage = "https://gtonkinhill.github.io/panaroo"
    url = "https://github.com/gtonkinhill/panaroo/archive/refs/tags/v1.2.10.tar.gz"

    license("MIT")

    version("1.2.10", sha256="066e5cd96b59918fa4fcd2dc12c92a273457ee17e2fe55576657c793566e948e")

    depends_on("python@3.6.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-plotly", type=("build", "run"))
    depends_on("py-dendropy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-gffutils", type=("build", "run"))
    depends_on("py-edlib", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-intbitset", type=("build", "run"))
    depends_on("cdhit", type=("build", "run"))
    depends_on("prokka", type=("build", "run"))
    depends_on("prank", type=("build", "run"))
    depends_on("mafft", type=("build", "run"))
    depends_on("clustal-omega", type=("build", "run"))
    depends_on("mash", type=("build", "run"))
