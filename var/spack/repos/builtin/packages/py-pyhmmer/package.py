# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyhmmer(PythonPackage):
    """HMMER is a biological sequence analysis tool that uses profile hidden
    Markov models to search for sequence homologs. HMMER3 is developed and
    maintained by the Eddy/Rivas Laboratory at Harvard University.  pyhmmer
    is a Python package, implemented using the Cython language, that provides
    bindings to HMMER3."""

    homepage = "https://github.com/althonos/pyhmmer"
    pypi = "pyhmmer/pyhmmer-0.10.14.tar.gz"

    license("MIT", checked_by="luke-dt")

    version("0.10.14", sha256="eb50bdfdf67a3b1fecfe877d7ca6d9bade9a9f3dea3ad60c959453bbb235573d")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@46.4:", type="build")
    depends_on("py-cython@3.0", type="build")
