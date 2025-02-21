# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProv(PythonPackage):
    """A Python library for W3C Provenance Data Model (PROV).

    A library for W3C Provenance Data Model supporting PROV-JSON, PROV-XML and
    PROV-O (RDF)
    """

    homepage = "https://prov.readthedocs.io/"
    pypi = "prov/prov-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="b6438f2195ecb9f6e8279b58971e02bc51814599b5d5383366eef91d867422ee")
    version("1.5.1", sha256="7a2d72b0df43cd9c6e374d815c8ce3cd5ca371d54f98f837853ac9fcc98aee4c")

    variant("dot", default=False, description="Graphical visualisation support for prov.model")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-lxml@3.3.5:", type=("build", "run"))
    depends_on("py-networkx@2.0:", type=("build", "run"))
    depends_on("py-python-dateutil@2.2:", type=("build", "run"))
    depends_on("py-rdflib@4.2.1:", type=("build", "run"))
    depends_on("py-pydot@1.2.0:", when="+dot", type=("build", "run"))
    depends_on("graphviz", when="+dot", type=("build", "run"))
