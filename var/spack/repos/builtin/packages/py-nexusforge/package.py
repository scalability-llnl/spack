# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNexusforge(PythonPackage):
    """Blue Brain Nexus Forge is a domain-agnostic, generic and
    extensible Python framework enabling non-expert users to create and
    manage knowledge graphs.
    """

    homepage = "https://github.com/BlueBrain/nexus-forge"
    pypi = "nexusforge/nexusforge-0.7.0.tar.gz"

    license("Apache-2.0")

    version("0.8.1", sha256="eb2909cbec185e7a73191c1be1e62902a0d8534f0d93454ef3e4e3b18b5129cf")
    version("0.8.0", sha256="4358505ead26e41c2a0c4e6113cf3a486c9661e2a3899394497a2b5a94b70424")
    version("0.7.0", sha256="a8d2951d9ad18df9f2f4db31a4c18fcdd27bfcec929b03a3c91f133ea439413c")

    variant("sklearn", default=False, description="Enable sklearn")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-hjson", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-nexus-sdk", type=("build", "run"))
    depends_on("py-aiohttp", type=("build", "run"))
    depends_on("py-rdflib@6.0.0:", type=("build", "run"))
    depends_on("py-rdflib@6.2.0", type=("build", "run"), when="@0.8.1")
    depends_on("py-rdflib@6.3.2", type=("build", "run"), when="@0.8.2:")
    depends_on("py-pyld", type=("build", "run"))
    depends_on("py-pyshacl@0.17.2", type=("build", "run"))
    depends_on("py-nest-asyncio@1.5.1:", type=("build", "run"))
    depends_on("py-pyparsing@2.0.2:", type=("build", "run"))
    depends_on("py-owlrl@5.2.3:", type=("build", "run"))
    depends_on("py-elasticsearch-dsl@7.4.0", type=("build", "run"))
    depends_on("py-scikit-learn", when="+sklearn", type="run")
