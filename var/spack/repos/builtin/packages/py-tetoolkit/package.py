# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTetoolkit(PythonPackage):
    """TEToolkit is a software package that utilizes both unambiguously
    (uniquely) and ambiguously (multi-) mapped reads to perform
    differential enrichment analyses from high throughput sequencing
    experiments."""

    homepage = "http://hammelllab.labsites.cshl.edu/software"
    pypi = "TEToolkit/TEToolkit-1.5.1.tar.gz"

    license("GPL-3.0-only")

    version("2.0.3", sha256="1d0f5928b30c6cd9dbef8e092ae0c11e9e707faf92a19af8eed3e360da7d4e46")
    version("1.5.1", sha256="22c13ca45bccc89e9d9bf48d59ae6db1fa4c634def64fc56ba9bffd23aa689ac")

    depends_on("py-setuptools")
    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("r-deseq", when="@:1.5.1", type=("build", "run"))
    depends_on("r-deseq2", when="@2.0.0:", type=("build", "run"))
