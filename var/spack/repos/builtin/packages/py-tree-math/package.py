# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTreeMath(PythonPackage):
    """Mathematical operations for JAX pytrees."""

    homepage = "https://github.com/google/tree-math"
    pypi = "tree-math/tree-math-0.2.0.tar.gz"

    license("Apache-2.0")

    version("0.2.0", sha256="fced2b436fa265b4e24ab46b5768d7b03a4a8d0b75de8a5ab110abaeac3b5772")

    depends_on("py-setuptools", type="build")
    depends_on("py-jax", type=("build", "run"))
