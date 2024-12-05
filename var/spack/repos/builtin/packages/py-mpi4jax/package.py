# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpi4jax(PythonPackage, CudaPackage):
    """Zero-copy MPI communication of JAX arrays, for turbo-charged HPC applications in
    Python."""

    homepage = "https://github.com/mpi4jax/mpi4jax"
    pypi = "mpi4jax/mpi4jax-0.3.11.post3.tar.gz"

    maintainers("bhaveshshrimali")

    license("MIT")

    version(
        "0.3.11.post3", sha256="ad4c5840c81ead40b68f4885d705c06eeca22cd4e998790de589c6566db75a75"
    )

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-cython@0.21:", type="build")
    depends_on("py-mpi4py@3.0.1:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-jax@0.3.25:", type=("build", "run"))

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            env.set("CUDA_PATH", self.spec["cuda"].prefix)
