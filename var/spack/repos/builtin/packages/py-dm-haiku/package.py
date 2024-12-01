# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDmHaiku(PythonPackage):
    """JAX-based neural network library"""

    homepage = "https://github.com/deepmind/dm-haiku"
    pypi = "dm-haiku/dm-haiku-0.0.5.tar.gz"

    license("Apache-2.0")

    version("0.0.12", sha256="ba0b3acf71433156737fe342c486da11727e5e6c9e054245f4f9b8f0b53eb608")
    version("0.0.7", sha256="86c34af6952a305a4bbfda6b9925998577acc4aa2ad9333da3d6047f4f8ed7c1")
    version("0.0.5", sha256="e986237e1f840aa3bd26217ecad84b611bf1456e2139f0f79ea71f9c6222d231")

    variant("jax", default=False, description="Build with JAX support", when="@0.0.12:")

    # setup.py
    depends_on("python@3.9:", when="@0.0.12:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # requirements.txt
    depends_on("py-absl-py@0.7.1:", type=("build", "run"))
    depends_on("py-jmp@0.0.2:", type=("build", "run"))
    depends_on("py-numpy@1.18.0:", type=("build", "run"))
    depends_on("py-tabulate@0.8.9:", type=("build", "run"))
    depends_on("py-flax@0.7.1:", when="@0.0.12:", type=("build", "run"))

    # requirements-jax.txt
    with when("+jax"):
        depends_on("py-jax@0.4.24:", type=("build", "run"))
        depends_on("py-jaxlib@0.4.24:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
    depends_on("py-jax", when="@:0.0.7", type=("build", "run"))

    # AttributeError: module 'jax' has no attribute 'xla'
    conflicts("^py-jax@0.4.14:", when="@:0.0.7")
