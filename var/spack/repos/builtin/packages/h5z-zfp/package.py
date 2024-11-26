# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class H5zZfp(CMakePackage):
    """A highly flexible floating point and integer compression plugin for the
    HDF5 library using ZFP compression."""

    homepage = "https://h5z-zfp.readthedocs.io/en/latest"
    git = "https://github.com/LLNL/H5Z-ZFP.git"
    url = "https://github.com/LLNL/H5Z-ZFP/archive/refs/tags/v1.1.1.tar.gz"

    maintainers("markcmiller86", "brtnfld", "byrnHDF")

    version("develop", branch="master")
    version("1.1.1", sha256="921af7b9d1c8c46c036b46544f2785f69d405c0701abe1c1ce3aca2bd5899171")
    version("1.1.0", sha256="48a81e69d1f3b61d9a1eb07e868164fadf3b88690ec930efd849f5889681a893")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=True, description="Enable Fortran support")

    depends_on("hdf5+fortran", when="+fortran")
    depends_on("hdf5", when="~fortran")
    depends_on("mpi", when="^hdf5+mpi")
    depends_on("zfp bsws=8")

    @property
    def make_defs(self):
        cc = spack_cc
        fc = spack_fc
        if self.spec.satisfies("^hdf5+mpi"):
            cc = self.spec["mpi"].mpicc
            fc = self.spec["mpi"].mpifc
        make_defs = [
            "PREFIX=%s" % prefix,
            "CC=%s" % cc,
            "HDF5_HOME=%s" % self.spec["hdf5"].prefix,
            "ZFP_HOME=%s" % self.spec["zfp"].prefix,
        ]

        if self.spec.satisfies("+fortran") and fc:
            make_defs += ["FC=%s" % fc]
        else:
            make_defs += ["FC="]

        return make_defs

    @property
    def build_targets(self):
        targets = ["all"]
        return self.make_defs + targets

    @property
    def install_targets(self):
        make_args = ["install"]
        return make_args + self.make_defs

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        make("check", *self.make_defs, parallel=False)
