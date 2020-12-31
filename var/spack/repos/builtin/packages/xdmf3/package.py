# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Xdmf3(CMakePackage):
    """XDMF, or eXtensible Data Model and Format (XDMF), is a common data model
       format to exchange scientific data between High Performance Computing
       codes and tools.
    """

    homepage = "http://xdmf.org"
    git = "https://gitlab.kitware.com/xdmf/xdmf.git"

    # There is no official release of XDMF and development has largely ceased,
    # but the current version, 3.x, is maintained on the master branch.
    version("2019-01-14", commit="8d9c98081d89ac77a132d56bc8bef53581db4078")

    variant("shared", default=True, description="Enable shared libraries")
    variant("mpi", default=True, description="Enable MPI")

    depends_on("libxml2")
    depends_on("boost")
    depends_on("libtiff")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5+mpi", when="+mpi")
    depends_on("hdf5~mpi", when="~mpi")

    patch("fix-libs.patch")

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

    @run_after("install")
    def post_install(self):
        if os.path.exists(self.prefix.lib):
            cmake_prefix = join_path(self.prefix.lib, "cmake")
        else:
            cmake_prefix = join_path(self.prefix.lib64, "cmake")

        # I need to create also the the related directory (Xdmf -> xdmf3)
        # to allow paraview to find the package
        new_dir_name = "xdmf3"
        mkdirp(join_path(cmake_prefix, new_dir_name))
        new_file_name = new_dir_name + "Config.cmake"

        # Copy here
        orig = join_path(cmake_prefix, "Xdmf", "XdmfConfig.cmake")
        dst = join_path(cmake_prefix, new_dir_name, new_file_name)
        force_symlink(orig, dst)

        # I also need to change the variables name in the folder "made for
        # Paraview" from 'XDMF_' to 'XDMF3_'Z
        filter_file("set(XDMF_", "set(XDMF3_", dst, string=True)
