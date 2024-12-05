# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyShortbred(PythonPackage):
    """ShortBRED is a system for profiling protein families of interest at
    very high specificity in shotgun meta'omic sequencing data."""

    homepage = "https://huttenhower.sph.harvard.edu/shortbred/"
    pypi = "shortbred/shortbred-0.9.5.tar.gz"

    license("MIT")

    version("0.9.5", sha256="a6ac09b858f14e2c0b8622b122ec91e5d02d32c12429cad66626d7ef26df10d5")

    depends_on("python@2.7.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-biopython@1.65:", type="run")
    depends_on("blast-plus@2.2.28:", type="run")
    depends_on("usearch@6.0.307:", type="run")
    depends_on("muscle@3.8.31:", type="run")
    depends_on("cdhit@4.6:", type="run")
