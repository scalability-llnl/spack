# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEdamOntology(PythonPackage):
    """Versioned, Python packaged EDAM ontology (http://edamontology.org/) data."""

    homepage = "https://github.com/edamontology/edam-ontology.py"
    pypi = "edam-ontology/edam-ontology-1.25.2.tar.gz"

    license("MIT")

    version("1.25.2", sha256="608c062ecb1ec260637645f73b4157d5abd47b19058a4ccca3bf292e373b8e06")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
