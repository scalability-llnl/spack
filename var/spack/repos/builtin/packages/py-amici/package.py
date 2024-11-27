# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAmici(PythonPackage):
    """Advanced Multilanguage Interface for CVODES and IDAS"""

    homepage = "https://github.com/AMICI-dev/AMICI"
    pypi = "amici/amici-0.11.28.tar.gz"

    version("0.16.0", sha256="1a2d6633ec34241d8d8b496d18d4318482cffe125e9ddf3ca6cac5d36d235f38")
    version("0.11.28", sha256="a8ddda70d8ebdc40600b4ad2ea02eb26e765ca0e594b957f61866b8c84255d5b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("boost", default=True, description="Enable boost support")
    variant("hdf5", default=True, description="Enable HDF5 support")

    depends_on("py-setuptools@48:", type=("build", "run"))

    depends_on("blas", type=("build", "run"))
    depends_on("boost", when="+boost", type=("build", "run"))
    depends_on("hdf5", when="+hdf5", type=("build", "run"))
    depends_on("swig@3.0:", type=("build", "run"))

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-sympy@1.9:", type=("build", "run"))
    depends_on("py-numpy@1.17.5:", when="^python@3.8", type=("build", "run"))
    depends_on("py-numpy@1.19.3:", when="^python@3.9", type=("build", "run"))
    depends_on("py-numpy@1.21.4:", when="^python@3.10:", type=("build", "run"))
    depends_on("py-python-libsbml", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pkgconfig", type=("build", "run"))
    depends_on("py-wurlitzer", type=("build", "run"))
    depends_on("py-toposort", type=("build", "run"))
    depends_on("py-mpmath", when="@0.16.0:", type=("build", "run"))

    def setup_run_environment(self, env):
        env.set("BLAS_LIBS", " ".join(self.spec["blas"].libs))

    def setup_build_environment(self, env):
        env.set("BLAS_LIBS", " ".join(self.spec["blas"].libs))
