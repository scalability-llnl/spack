# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylcUiserver(PythonPackage):
    """Cylc UI Server."""

    homepage = "https://github.com/cylc/cylc-uiserver/"
    pypi = "cylc-uiserver/cylc-uiserver-1.3.0.tar.gz"
    git = "https://github.com/cylc/cylc-uiserver.git"

    maintainers("LydDeb", "climbfuji")

    license("GPL-3.0-or-later")

    # Version 1.5.1 is available at PyPI, but not at the URL that is considered canonical by Spack
    # https://github.com/spack/spack/issues/48479
    version("1.5.1", commit="3a41c6fbefbcea33c41410f3698de8b62c9871b8")
    version("1.3.0", sha256="f3526e470c7ac2b61bf69e9b8d17fc7a513392219d28baed9b1166dcc7033d7a")

    depends_on("python@3.8:", when="@1.5.1", type=("build", "run"))
    depends_on("py-wheel", type="build")
    depends_on("py-setuptools@40.9.0:", type="build")

    depends_on("py-cylc-flow@8.2", when="@1.3.0", type=("build", "run"))
    depends_on("py-cylc-flow@8.3", when="@1.5.1", type=("build", "run"))
    depends_on("py-ansimarkup@1.0.0:", type=("build", "run"))
    depends_on("py-graphene", type=("build", "run"))
    depends_on("py-graphene-tornado@2.6", type=("build", "run"))
    depends_on("py-graphql-ws@0.4.4", type=("build", "run"))
    depends_on("py-jupyter-server@1.10.2:1", when="@1.3.0", type=("build", "run"))
    depends_on("py-jupyter-server@2.7:", when="@1.5.1", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-psutil", when="@1.5.1", type=("build", "run"))
    depends_on("py-tornado@6.1.0:", type=("build", "run"))
    depends_on("py-traitlets@5.2.1:", type=("build", "run"))
    depends_on("py-pyzmq", type=("build", "run"))
    depends_on("py-graphql-core", type=("build", "run"))
    depends_on("py-rx@:1", type=("build", "run"))
