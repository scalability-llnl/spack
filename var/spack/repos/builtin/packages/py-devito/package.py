# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDevito(PythonPackage):
    """Devito is a Python package to implement optimized stencil computation.

    (e.g., finite differences, image processing, machine learning) from high-level
    symbolic problem definitions. Devito builds on SymPy and employs automated code
    generation and just-in-time compilation to execute optimized computational kernels
    on several computer platforms, including CPUs, GPUs, and clusters thereof.
    """

    homepage = "https://www.devitoproject.org/"
    pypi = "devito/devito-4.8.1.tar.gz"

    license("MIT")

    version("4.8.1", sha256="56d0957a3226ed2a81c408107a614f04faa896d42c83a8b2bd1c8b1100adf51d")

    variant("mpi", default=False, description="Enable MPI support")
    variant("optional", default=False, description="Enable matplolib & pandas support")

    depends_on("py-pip@9.0.1:", type="build")
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-sympy@1.9:1.11", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-flake8@2.1.0:", type=("build", "run"))
    depends_on("py-nbval", type=("build", "run"))
    depends_on("py-cached-property", type=("build", "run"))
    depends_on("py-psutil@5.1.0:5", type=("build", "run"))
    depends_on("py-py-cpuinfo@:9", type=("build", "run"))
    depends_on("py-cgen@2020.1:", type=("build", "run"))
    depends_on("py-codepy@2019.1:", type=("build", "run"))
    depends_on("py-click@:8", type=("build", "run"))
    depends_on("py-multidict", type=("build", "run"))
    depends_on("py-anytree@2.4.3:2.8", type=("build", "run"))
    depends_on("py-pyrevolve@2.1.3:", type=("build", "run"))
    depends_on("py-distributed@:2023.3", type=("build", "run"))
    depends_on("py-pytest@7.2:7", type=("build", "run"))
    depends_on("py-pytest-runner", type=("build", "run"))
    depends_on("py-pytest-cov", type=("build", "run"))

    # requirements-mpi.txt
    depends_on("py-mpi4py@:3", type=("build", "run"), when="+mpi")
    depends_on("py-ipyparallel@:8.5", type=("build", "run"), when="+mpi")

    # requirements-optional.txt
    depends_on("py-matplotlib", type=("build", "run"), when="+optional")
    depends_on("py-pandas", type=("build", "run"), when="+optional")

    depends_on("mpi", type=("build", "run"), when="+mpi")

    depends_on("intel-parallel-studio", type="run", when="%intel@:2021.1.1")
    depends_on("intel-oneapi-compilers", type="run", when="%intel@2021.1.2:")

    patch("4.8.1.patch", when="@4.8.1")

    @run_before("install")
    def add_examples_dir(self):
        # Add file `__init__py` to examples/ so it is picked up by setuptools
        touch("examples/__init__.py")

    def setup_run_environment(self, env):
        # Make benchmark.py available
        env.prepend_path("DEVITO_HOME", self.prefix)
