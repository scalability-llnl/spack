# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlax(PythonPackage):
    """Flax: A neural network library for JAX designed for flexibility."""

    homepage = "https://github.com/google/flax"
    pypi = "flax/flax-0.8.1.tar.gz"

    license("Apache-2.0")

    version("0.8.5", sha256="4a9cb7950ece54b0addaa73d77eba24e46138dbe783d01987be79d20ccb2b09b")
    version("0.8.1", sha256="ce3d99e9b4c0d2e4d9fc28bc56cced8ba953adfd695aabd24f096b4c8a7e2f92")
    version("0.7.3", sha256="e9dbc7eb6c80d31277f97b626c07978d2a84f1bb635cf05957a02a3a496493e6")

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:", when="@0.8:")
        depends_on("py-numpy@1.26.0:", when="@0.8: ^python@3.12:")
        depends_on("py-numpy@1.23.2:", when="@0.8: ^python@3.11:")
        depends_on("py-numpy@1.22:", when="@0.8:")
        depends_on("py-numpy@1.12:")
        depends_on("py-jax@0.4.27:", when="@0.8.5:")
        depends_on("py-jax@0.4.19:", when="@0.8:")
        depends_on("py-jax@0.4.2:")
        depends_on("py-msgpack")
        depends_on("py-optax")
        depends_on("py-orbax-checkpoint")
        depends_on("py-tensorstore")
        depends_on("py-rich@11.1:")
        depends_on("py-typing-extensions@4.2:")
        depends_on("py-pyyaml@5.4.1:")
