# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyfr(PythonPackage, CudaPackage, ROCmPackage):
    """PyFR is an open-source Python based framework for solving
    advection-diffusion type problems on streaming architectures
    using the Flux Reconstruction approach of Huynh."""

    homepage = "https://www.pyfr.org/"
    pypi = "pyfr/pyfr-1.13.0.tar.gz"
    git = "https://github.com/PyFR/PyFR/"
    maintainers("MichaelLaufer")

    license("BSD-3-Clause")

    # git branches
    version("develop", branch="develop")
    version("master", branch="master")

    # pypi releases
    version(
        "2.0.3",
        sha256="1fd2ca377596ab541d929d2c7b2d27e376e21b5dd6c4c0e7653bbb53864dee61",
        preferred=True,
    )
    version("2.0.2", sha256="2c6bf460ffec446a933451792c09d3cd85d6703f14636d99810d61823b8d92c7")
    version("1.15.0", sha256="6a634b9d32447f45d3c24c9de0ed620a0a0a781be7cc5e57b1c1bf44a4650d8d")
    version("1.14.0", sha256="ebf40ce0896cce9ac802e03fd9430b5be30ea837c31224531a6d5fd68f820766")
    version("1.13.0", sha256="ac6ecec738d4e23799ab8c50dea9bdbd7d37bc971bd33f22720c5a230b8e7b2f")

    variant("metis", default=False, when="@:1.15.0", description="Metis for mesh partitioning")
    variant("scotch", default=True, description="Scotch for mesh partitioning")
    variant("cuda", default=False, description="CUDA backend support")
    variant("hip", default=False, description="HIP backend support")
    variant("libxsmm", default=True, description="LIBXSMM for OpenMP backend")

    # Required dependencies
    depends_on("python@3.9:", when="@:1.15.0", type=("build", "run"))
    depends_on("python@3.10:", when="@2.0.2:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-gimmik@2.3:2", when="@:1.14.0", type=("build", "run"))
    depends_on("py-gimmik@3", when="@1.15.0", type=("build", "run"))
    depends_on("py-gimmik@3.2.1:", when="@2.0.2:", type=("build", "run"))
    depends_on("py-h5py@2.10:", type=("build", "run"))
    depends_on("py-mako@1.0.0:", type=("build", "run"))
    depends_on("py-mpi4py@3.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.20:", when="@:1.15.0", type=("build", "run"))
    depends_on("py-numpy@1.26.4:", when="@2.0.2:", type=("build", "run"))
    depends_on("py-platformdirs@2.2.0:", type=("build", "run"))
    depends_on("py-pytools@2016.2.1:", type=("build", "run"))
    depends_on("py-rtree@1.0.1:", when="@2.0.2:", type=("build", "run"))

    # Optional dependencies
    depends_on("metis@5.0.0:5.1.0", when="@:1.15.0 +metis", type=("run"))
    depends_on("scotch@7.0.1: +link_error_lib", when="+scotch", type=("run"))
    depends_on("cuda@8.0: +allow-unsupported-compilers", when="@:1.14.0 +cuda", type=("run"))
    depends_on("cuda@11.4.0: +allow-unsupported-compilers", when="@1.15.0: +cuda", type=("run"))
    depends_on("rocblas@5.2.0:", when="@:1.15.0 +hip", type=("run"))
    depends_on("rocblas@6.0.0:", when="@2.0.2: +hip", type=("run"))
    depends_on("libxsmm@1.18:+shared blas=0", when="+libxsmm", type=("run"))

    # Explicitly add dependencies to environment variables
    def setup_run_environment(self, env):
        deps = ["metis", "scotch", "libxsmm", "hip", "rocblas"]
        pyfr_library_path = []
        for dep in deps:
            if "+{}".format(dep) in self.spec:
                pyfr_library_path.extend(self.spec[dep].libs.directories)
        env.set("PYFR_LIBRARY_PATH", ":".join(pyfr_library_path))

        # LD_LIBRARY_PATH needed for cuda
        if "+cuda" in self.spec:
            env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].libs.directories[0])
