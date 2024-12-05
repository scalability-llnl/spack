# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Xdmf3(CMakePackage):
    """XDMF, or eXtensible Data Model and Format (XDMF), is a common data model
    format to exchange scientific data between High Performance Computing
    codes and tools.
    """

    homepage = "https://xdmf.org"
    git = "https://gitlab.kitware.com/xdmf/xdmf.git"

    license("BSD-3-Clause")

    # There is no official release of XDMF and development has largely ceased,
    # but the current version, 3.x, is maintained on the master branch.
    version("2019-01-14", commit="8d9c98081d89ac77a132d56bc8bef53581db4078")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Enable shared libraries")
    variant("mpi", default=True, description="Enable MPI")

    depends_on("libxml2")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("mpi", when="+mpi")
    depends_on("hdf5@1.10:+mpi", when="+mpi")
    depends_on("hdf5@1.10:~mpi", when="~mpi")
    # motivated by discussion in https://gitlab.kitware.com/xdmf/xdmf/-/issues/28
    patch("fix_hdf5_hid_t.diff")

    def cmake_args(self):
        """Populate cmake arguments for XDMF."""
        spec = self.spec

        cmake_args = [
            "-DBUILD_SHARED_LIBS=%s" % str("+shared" in spec),
            "-DXDMF_BUILD_UTILS=ON",
            "-DXDMF_WRAP_JAVA=OFF",
            "-DXDMF_WRAP_PYTHON=OFF",
            "-DXDMF_BUILD_TESTING=OFF",
        ]

        return cmake_args
