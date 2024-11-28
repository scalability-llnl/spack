# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJraph(PythonPackage):
    """Jraph: A library for Graph Neural Networks in Jax."""

    homepage = "https://github.com/deepmind/jraph"
    pypi = "jraph/jraph-0.0.6.dev0.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.6.dev0", sha256="c3ac3a0b224b344eb6d367e8bc312d95ea41bf825d01ea31b80dd8c22c0dd8b8"
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-jax@0.1.55:", type=("build", "run"))
    depends_on("py-jaxlib@0.1.37:", type=("build", "run"))
    depends_on("py-numpy@1.18:", type=("build", "run"))
