# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNanoplot(PythonPackage):
    """Plotting scripts for long read sequencing data"""

    homepage = "https://github.com/wdecoster/NanoPlot"
    pypi = "NanoPlot/nanoplot-1.43.0.tar.gz"

    maintainers("Pandapip1")

    version("1.43.0", sha256="0f94096d689b552c32fd7246ad87cb6d5e5e2499dad5acc551091e0ff67f48df")
    version("1.42.0", sha256="0f8fd2cffd33a346b3306716058c6cb4091c931e8ab502f10b17a28749e8b6d9")

    depends_on("py-setuptools", type=("build",))
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-pysam@0.10.0.1:", type=("build", "run"))
    depends_on("py-pandas@1.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.16.5:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-nanoget@1.19.1:", type=("build", "run"))
    depends_on("py-nanomath@1.0.0:", type=("build", "run"), when="@:1.42")
    depends_on("py-plotly@5.4.0:", type=("build", "run"))
    depends_on("py-pyarrow", type=("build", "run"))
    depends_on("py-kaleido", type=("build", "run"))
