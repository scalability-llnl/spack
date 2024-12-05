# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRdflibJsonld(PythonPackage):
    """rdflib extension adding JSON-LD parser and serializer"""

    homepage = "https://github.com/RDFLib/rdflib-jsonld"
    pypi = "rdflib-jsonld/rdflib-jsonld-0.6.2.tar.gz"

    license("BSD-3-Clause")

    version("0.6.2", sha256="107cd3019d41354c31687e64af5e3fd3c3e3fa5052ce635f5ce595fd31853a63")
    version("0.6.0", sha256="03af8b5540a8e7bb0dae0d9ba1a3bd7f6435abd82cfb4b3ad5e0cdb1bf45a2a6")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-rdflib@5.0.0:", type=("build", "run"))
