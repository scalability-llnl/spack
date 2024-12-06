# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylcUiserver(PythonPackage):
    """Cylc UI Server."""

    homepage = "https://github.com/cylc/cylc-uiserver/"
    pypi = "cylc-uiserver/cylc-uiserver-1.3.0.tar.gz"

    maintainers("LydDeb")

    license("GPL-3.0-or-later")

    version("1.3.0", sha256="f3526e470c7ac2b61bf69e9b8d17fc7a513392219d28baed9b1166dcc7033d7a")

    depends_on("py-wheel", type="build")
    depends_on("py-setuptools@40.9.0:", type="build")
    depends_on("py-cylc-flow@8.2", type=("build", "run"))
    depends_on("py-ansimarkup@1.0.0:", type=("build", "run"))
    depends_on("py-graphene", type=("build", "run"))
    depends_on("py-graphene-tornado@2.6", type=("build", "run"))
    depends_on("py-graphql-ws@0.4.4", type=("build", "run"))
    depends_on("py-jupyter-server@1.10.2:1", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-tornado@6.1.0:", type=("build", "run"))
    depends_on("py-traitlets@5.2.1:", type=("build", "run"))
    depends_on("py-pyzmq", type=("build", "run"))
    depends_on("py-graphql-core", type=("build", "run"))
    depends_on("py-rx@:1", type=("build", "run"))
