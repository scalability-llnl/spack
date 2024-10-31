# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BufrQuery(CMakePackage, PythonExtension):
    """The NOAA bufr-query Library can be used to read NCEP and WMO formated BUFR
    files using a simple interface that does not require the user to know the
    details of the BUFR format. Detailed documentation for the BUFR Library can
    be found at https://bufr-query.readthedocs.io/en/latest/index.html"""

    homepage = "https://github.com/NOAA-EMC/bufr-query"
    url = "https://github.com/NOAA-EMC/bufr-query/archive/refs/tags/v0.0.1.tar.gz"
    maintainers("srherbener", "rmclaren")

    license("Apache-2.0", checked_by="srherbener")

    version("0.0.3", sha256="f2952a190cc1d7714a3bfe481fb1545459639ba304fc31b941062b471dea1d41")
    version("0.0.2", sha256="b87a128246e79e3c76e3158d89823e2ae38e9ee1a5a81b6f7b423837bdb93a1f")
    version("0.0.1", sha256="001990d864533c101b93d1c351edf50cf8b5ccc575e442d174735f6c332d3d03")

    # Required dependencies
    depends_on("ecbuild", type=("build"))
    depends_on("llvm-openmp", when="%apple-clang", type=("build", "run"))
    depends_on("mpi", type=("build", "run"))
    depends_on("eckit@1.24.4:", type=("build", "run"))
    depends_on("eigen@3:", type=("build", "run"))
    depends_on("gsl-lite", type=("build", "run"))
    depends_on("netcdf-c", type=("build", "run"))
    depends_on("netcdf-cxx4", type=("build", "run"))
    depends_on("bufr", type=("build", "run"))

    # Optional dependencies
    variant("python", default=True, description="Enable Python interface")

    with when("+python"):
        extends("python")
        depends_on("py-pybind11", type="build")

    # Patches
    patch(
        "https://github.com/NOAA-EMC/bufr-query/pull/20.patch?full_index=1",
        sha256="3acf11082c9e76e64dbbda4f62ac0cbc234dca7e60c85a275e778417cfd65001",
        when="+python @:0.0.2",
    )

    # CMake configuration
    def cmake_args(self):
        args = [self.define_from_variant("BUILD_PYTHON_BINDINGS", "python")]

        # provide path to netcdf-c include files
        nc_include_dir = Executable("nc-config")("--includedir", output=str).strip()
        args.append("-DCMAKE_C_FLAGS=-I" + nc_include_dir)
        args.append("-DCMAKE_CXX_FLAGS=-I" + nc_include_dir)

        return args
