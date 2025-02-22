# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPerfdump(CMakePackage):
    """An MPI- and HDF5- enabled Python module to create PAPI dumps"""

    homepage = "https://github.com/RECUP-DOE/pyperfdump/"
    git = "https://github.com/RECUP-DOE/pyperfdump.git"
    url = "https://github.com/RECUP-DOE/pyperfdump/archive/refs/tags/v1.1.tar.gz"

    maintainers("chaseleif")

    license("Apache-2.0 WITH LLVM-Exception", checked_by="chaseleif")

    version("1.1", sha256="d2d96e2bd8ba2616ea4a44233ea240a529788390a5c22d35f9de79a22647370d")

    variant("mpi", default=False, description="Use MPI")
    variant("hdf5", default=False, description="Enable HDF5 output")

    depends_on("cmake@3.15:", type="build")
    depends_on("cxx", type="build")
    depends_on("papi", type=("build", "link", "run"))
    depends_on("python@3:", type=("build", "link", "run"))

    depends_on("mpi", type=("build", "link", "run"), when="+mpi")
    depends_on("py-mpi4py", type="run", when="+mpi")

    depends_on("hdf5+mpi", type=("build", "link", "run"), when="+mpi+hdf5")
    depends_on("hdf5~mpi", type=("build", "link", "run"), when="~mpi+hdf5")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DCMAKE_INSTALL_RPATH={0}".format(spec.prefix.lib),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define_from_variant("ENABLE_HDF5", "hdf5"),
            "-DPython_ROOT_DIR={0}".format(spec["python"].prefix),
            "-DPAPI_PREFIX={0}".format(spec["papi"].prefix),
        ]
        if "+mpi" in spec:
            args.append("-DMPI_HOME={0}".format(spec["mpi"].prefix))
        if "+hdf5" in spec:
            args.append("-DHDF5_ROOT={0}".format(spec["hdf5"].prefix))
        return args
