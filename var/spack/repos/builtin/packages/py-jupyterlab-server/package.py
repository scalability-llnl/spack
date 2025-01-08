# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlabServer(PythonPackage):
    """A set of server components for JupyterLab and JupyterLab
    like applications"""

    homepage = "https://github.com/jupyterlab/jupyterlab_server"
    pypi = "jupyterlab_server/jupyterlab_server-1.2.0.tar.gz"

    license("BSD-3-Clause")

    version("2.27.3", sha256="eb36caca59e74471988f0ae25c77945610b887f777255aa21f8065def9e51ed4")
    version("2.27.2", sha256="15cbb349dc45e954e09bacf81b9f9bcb10815ff660fb2034ecd7417db3a7ea27")
    version("2.27.1", sha256="097b5ac709b676c7284ac9c5e373f11930a561f52cd5a86e4fc7e5a9c8a8631d")
    version("2.27.0", sha256="b03382075545981dd0ab7a9e4ffff74b6ed2b424c92e32fcc1c0bd65dafcb56d")
    version("2.26.0", sha256="9b3ba91cf2837f7f124fca36d63f3ca80ace2bed4898a63dd47e6598c1ab006f")
    version("2.25.4", sha256="2098198e1e82e0db982440f9b5136175d73bea2cd42a6480aa6fd502cb23c4f9")
    version("2.25.0", sha256="77c2f1f282d610f95e496e20d5bf1d2a7706826dfb7b18f3378ae2870d272fb7")
    version("2.24.0", sha256="4e6f99e0a5579bbbc32e449c4dbb039561d4f1a7827d5733273ed56738f21f07")
    version("2.23.0", sha256="83c01aa4ad9451cd61b383e634d939ff713850f4640c0056b2cdb2b6211a74c7")
    version("2.22.1", sha256="dfaaf898af84b9d01ae9583b813f378b96ee90c3a66f24c5186ea5d1bbdb2089")
    version("2.10.3", sha256="3fb84a5813d6d836ceda773fb2d4e9ef3c7944dbc1b45a8d59d98641a80de80a")
    version("2.6.0", sha256="f300adf6bb0a952bebe9c807a3b2a345d62da39b476b4f69ea0dc6b5f3f6b97d")
    version("1.2.0", sha256="5431d9dde96659364b7cc877693d5d21e7b80cea7ae3959ecc2b87518e5f5d8c")
    version("1.1.0", sha256="bac27e2ea40f686e592d6429877e7d46947ea76c08c878081b028c2c89f71733")

    depends_on("python@3.8:", when="@2.25:")
    depends_on("python@3.7:", when="@2.22:")
    depends_on("py-hatchling@1.7:", when="@2.25:", type="build")
    depends_on("py-hatchling@1.5:", when="@2.16:", type="build")

    with when("@:2.14"):
        depends_on("py-setuptools", type="build")
        depends_on("py-jupyter-packaging@0.10:1", when="@2.10.3", type="build")
        depends_on("py-jupyter-packaging@0.9:0", when="@:2.6", type="build")

    depends_on("py-babel@2.10:", when="@2.16.4:", type=("build", "run"))
    depends_on("py-babel", when="@2.5.1:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8.3:", when="@2.13: ^python@:3.9", type=("build", "run"))
    depends_on("py-jinja2@3.0.3:", when="@2.11:", type=("build", "run"))
    depends_on("py-jinja2@2.10:", type=("build", "run"))
    depends_on("py-json5@0.9.0:", when="@2.16.4:", type=("build", "run"))
    depends_on("py-json5", type=("build", "run"))
    depends_on("py-jsonschema@4.18:", when="@2.25:", type=("build", "run"))
    depends_on("py-jsonschema@4.17.3:", when="@2.17:", type=("build", "run"))
    depends_on("py-jsonschema@3.0.1:", type=("build", "run"))
    depends_on("py-jupyter-server@1.21:2", when="@2.16.4:", type=("build", "run"))
    depends_on("py-jupyter-server@1.4:1", when="@2.5.1:2.10", type=("build", "run"))
    depends_on("py-packaging@21.3:", when="@2.16.4:", type=("build", "run"))
    depends_on("py-packaging", when="@2.5.1:", type=("build", "run"))
    depends_on("py-requests@2.31:", when="@2.25:", type=("build", "run"))
    depends_on("py-requests@2.28:", when="@2.16.4:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))

    # old dependencies
    depends_on("py-entrypoints@0.2.2:", when="@2.7:2.12", type=("build", "run"))
    depends_on("py-notebook@4.2.0:", when="@:2.5.0", type=("build", "run"))
