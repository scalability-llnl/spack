# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHeat(PythonPackage):
    """Heat is a flexible and seamless open-source software for high performance data analytics
    and machine learning. It provides highly optimized algorithms and data structures for tensor
    computations using CPUs, GPUs and distributed cluster systems on top of MPI."""

    homepage = "https://github.com/helmholtz-analytics/heat/"
    pypi = "heat/heat-1.3.0.tar.gz"

    maintainers("mrfh92", "ClaudiaComito", "JuanPedroGHM")

    license("MIT")

    version("1.4.2", sha256="d6714428a9c5204c1c44a2b246f228effaddc688f812277f229f4acdbcfeb7c5")
    version("1.4.1", sha256="ecd871717c372a6983f643c0178dda44bc017d6b32b9258dbf3775af95f580ce")
    version("1.4.0", sha256="6836fa10f9ce62ea61cf1bdc3283d7ad0c305836cc5a08c4edfd30695708e788")
    version("1.3.1", sha256="8997ddc56a1d3078b44a1e2933adc0a7fbf678bd19bade3ae015bc0e13d40d3b")
    version("1.3.0", sha256="fa247539a559881ffe574a70227d3c72551e7c4a9fb29b0945578d6a840d1c87")

    variant("docutils", default=False, description="Use the py-docutils package")
    variant("hdf5", default=False, description="Use the py-h5py package needed for HDF5 support")
    variant(
        "netcdf", default=False, description="Use the py-netcdf4 package needed for NetCDF support"
    )
    variant("dev", default=False, description="Use the py-pre-commit package")
    variant(
        "examples",
        default=False,
        description="Use py-scikit-learn and py-matplotlib for the example tests",
    )

    depends_on("py-setuptools", type="build")

    with when("@1.3"):
        depends_on("python@3.8:3.10", type=("build", "run"))
        depends_on("py-mpi4py@3:", type=("build", "run"))
        depends_on("py-numpy@1.20:1", type=("build", "run"))
        depends_on("py-torch@1.8:2.0.1", type=("build", "run"))
        depends_on("py-scipy@0.14:", type=("build", "run"))
        depends_on("pil@6:", type=("build", "run"))
        depends_on("py-torchvision@0.8:", type=("build", "run"))

    with when("@1.4"):
        depends_on("python@3.8:3.11", type=("build", "run"))
        depends_on("py-mpi4py@3:", type=("build", "run"))
        depends_on("py-numpy@1.22:1", type=("build", "run"))
        depends_on("py-torch@1.11:2.3.2", type=("build", "run"))
        depends_on("py-scipy@1.10:", type=("build", "run"))
        depends_on("pil@6:", type=("build", "run"))
        depends_on("py-torchvision@0.12:", type=("build", "run"))

    depends_on("py-docutils@0.16:", when="+docutils", type=("build", "link", "run"))
    depends_on("py-h5py@2.8.0:", when="+hdf5", type=("build", "link", "run"))
    depends_on("py-netcdf4@1.5.6:", when="+netcdf", type=("build", "link", "run"))
    depends_on("py-pre-commit@1.18.3:", when="+dev", type=("build", "link", "run"))
    depends_on("py-scikit-learn@0.24.0:", when="+examples", type=("build", "link", "run"))
    depends_on("py-matplotlib@3.1.0:", when="+examples", type=("build", "link", "run"))
