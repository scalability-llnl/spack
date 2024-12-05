# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeneimpacts(PythonPackage):
    """Given multiple snpEff or VEP or BCFTools consequence annotations
    for a single variant, get an orderable python object for each annotation.
    """

    homepage = "https://github.com/brentp/geneimpacts"
    url = "https://github.com/brentp/geneimpacts/archive/v0.3.7.tar.gz"

    license("MIT")

    version("0.3.7", sha256="895a0aa64935bf8528257fc5a3747c09adbf30c4885d95b0fa69ba4bb858c133")
    version("0.3.6", sha256="7998e469e7c25b15ecb1d7a73620cc42f13ca91f3f49384513729c180e3a9b97")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
