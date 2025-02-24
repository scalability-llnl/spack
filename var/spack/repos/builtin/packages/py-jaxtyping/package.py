# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaxtyping(PythonPackage):
    """Type annotations and runtime checking for shape and dtype of JAX arrays, and PyTrees."""

    homepage = "https://docs.kidger.site/jaxtyping/"
    pypi = "jaxtyping/jaxtyping-0.2.33.tar.gz"

    license("Apache-2.0")

    version("0.2.33", sha256="9a9cfccae4fe05114b9fb27a5ea5440be4971a5a075bbd0526f6dd7d2730f83e")
    version("0.2.19", sha256="21ff4c3caec6781cadfe980b019dde856c1011e17d11dfe8589298040056325a")

    depends_on("py-hatchling", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:3", when="@0.2.33:")
        depends_on("python@3.8:3", when="@0.2.19")
        depends_on("py-typeguard@2.13.3", when="@0.2.33:")
        depends_on("py-typeguard@2.13.3:", when="@0.2.19")

        # Historical dependencies
        depends_on("py-numpy@1.12:", when="@0.2.19")
        depends_on("py-typing-extensions@3.7.4.1:", when="@0.2.19")
