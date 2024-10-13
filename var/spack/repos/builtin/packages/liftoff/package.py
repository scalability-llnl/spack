# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liftoff(PythonPackage):
    """Liftoff is a tool that accurately maps annotations in GFF or
    GTF between assemblies of the same, or closely-related species.
    """

    homepage = "https://github.com/agshumate/Liftoff"

    pypi = "liftoff/Liftoff-1.6.3.2.tar.gz"

    git = "https://github.com/agshumate/Liftoff.git"

    maintainers("snehring")

    license("GPL-3.0-only", checked_by="snehring")

    version("1.6.3.2", sha256="7070a861144d0f043533893d39f95589a64d63f0365a99d06d71f1700b7fb758")

    depends_on("python@3:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.22:", type=("build", "run"))
    depends_on("py-biopython@1.76:", type=("build", "run"))
    depends_on("py-gffutils@0.10.1:", type=("build", "run"))
    depends_on("py-networkx@2.4:", type=("build", "run"))
    depends_on("py-pysam@0.19.1:", type=("build", "run"))
    depends_on("py-pyfaidx@0.5.8:", type=("build", "run"))
    depends_on("py-interlap@0.2.6:", type=("build", "run"))
    depends_on("py-ujson@3:", type=("build", "run"))
    depends_on("py-parasail@1.2.1:", type=("build", "run"))
    depends_on("minimap2", type="run")
