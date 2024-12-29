# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumba4jax(PythonPackage):
    """Use numba-compiled kernels from within Jax"""

    homepage = "https://github.com/PhilipVinc/numba4jax"
    pypi = "numba4jax/numba4jax-0.0.12.tar.gz"

    license("MIT")

    version("0.0.12", sha256="e1faf6a0566f4fb941abf8821b9c854b7398eb08a0c8157927f8b4717a393446")

    with default_args(type="build"):
        depends_on("py-hatchling@1.8.0:")
        depends_on("py-hatch-vcs")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")
        depends_on("py-numpy@1.22:1.23")
        depends_on("py-numba@0.53:0.61")
        depends_on("py-cffi@1.14.4:")
        depends_on("py-jax@0.4.16:0.5")
        depends_on("py-jaxlib@0.4.16:0.5")
