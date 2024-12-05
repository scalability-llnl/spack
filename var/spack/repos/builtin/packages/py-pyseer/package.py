# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyseer(PythonPackage):
    """Sequence Elements Enrichment Analysis (SEER), python implementation"""

    homepage = "https://pyseer.readthedocs.io/en/master/"

    # Not availible on PyPI
    url = "https://github.com/mgalardini/pyseer/releases/download/1.3.11/pyseer-1.3.11.tar.gz"

    version("1.3.11", sha256="384313a3a14b92f873eaad53f77a319d90b584b9253785a7ca1dfc7d9220c91e")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-statsmodels@0.10.0:", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-dendropy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pybedtools", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-glmnet-python@1.0.2", type=("build", "run"))
