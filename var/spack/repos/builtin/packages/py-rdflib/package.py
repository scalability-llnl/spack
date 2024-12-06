# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRdflib(PythonPackage):
    """RDFLib is a pure Python package for working with RDF. RDFLib
       contains most things you need to work with RDF, including:
    parsers and serializers for RDF/XML, N3, NTriples, N-Quads,
    Turtle, TriX, Trig and JSON-LD (via a plugin).  a Graph interface
    which can be backed by any one of a number of Store
    implementations store implementations for in-memory storage and
    persistent storage on top of the Berkeley DB a SPARQL 1.1
    implementation - supporting SPARQL 1.1 Queries and Update
    statements"""

    homepage = "https://github.com/RDFLib/rdflib"
    pypi = "rdflib/rdflib-5.0.0.tar.gz"

    license("BSD-3-Clause")

    version("7.0.0", sha256="9995eb8569428059b8c1affd26b25eac510d64f5043d9ce8c84e0d0036e995ae")
    version("6.3.2", sha256="72af591ff704f4caacea7ecc0c5a9056b8553e0489dd4f35a9bc52dbd41522e0")
    version("6.2.0", sha256="62dc3c86d1712db0f55785baf8047f63731fa59b2682be03219cb89262065942")
    version("6.0.2", sha256="6136ae056001474ee2aff5fc5b956e62a11c3a9c66bb0f3d9c0aaa5fbb56854e")
    version("5.0.0", sha256="78149dd49d385efec3b3adfbd61c87afaf1281c30d3fcaf1b323b34f603fb155")

    depends_on("python@3.7:3", when="@6.3:", type=("build", "run"))
    depends_on("python@3.8.1:3", when="@7:", type=("build", "run"))
    depends_on("py-poetry-core@1.4:", when="@6.3:", type="build")

    depends_on("py-isodate@0.6", when="@6.3:", type=("build", "run"))
    depends_on("py-isodate", type=("build", "run"))
    depends_on("py-pyparsing@2.1:3", when="@6.3:", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-importlib-metadata@4", when="@6.3: ^python@:3.7", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@6.1: ^python@:3.7", type=("build", "run"))

    # Historical dependencies
    depends_on("py-setuptools", when="@6:6.2", type=("build", "run"))
    depends_on("py-setuptools", when="@:5", type="build")
    depends_on("py-six", when="@:5", type=("build", "run"))
