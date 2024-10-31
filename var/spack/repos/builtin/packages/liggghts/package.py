# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from glob import glob

from spack.package import *


class Liggghts(MakefilePackage):
    """Discrete element method particle simulation."""

    homepage = "https://www.cfdem.com/media/DEM/docu/Manual.html"
    url = "https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/archive/3.8.0.tar.gz"
    git = "ssh://git@github.com/CFDEMproject/LIGGGHTS-PUBLIC.git"

    maintainers("SofiaXu")

    license("GPL-2.0-only")

    version("3.8.0", sha256="9cb2e6596f584463ac2f80e3ff7b9588b7e3638c44324635b6329df87b90ab03")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")
    variant("jpeg", default=True, description="Enable JPEG support")
    variant("gzip", default=True, description="Enable GZIP for some input and output files")
    variant("debug", default=False, description="Builds a debug version of the executable")
    variant("profile", default=False, description="Generate profiling code")

    depends_on("vtk@6.1.0:8.2.0")
    depends_on("mpi", when="+mpi")
    depends_on("jpeg", when="+jpeg")
    depends_on("zlib-api", when="+gzip")
    # patch for makefile test code
    patch("makefile.patch")
    # patch for clang and oneapi
    patch("makefile-llvm-based-compiler.patch", when="%clang")
    patch("makefile-llvm-based-compiler.patch", when="%oneapi")
    # C++17 support
    patch("cpp-17.patch")
    build_directory = "src"
    build_targets = ["auto"]

    def edit(self, spec, prefix):
        # The package expects you to create Makefile.user from
        # Makefile.user_default.
        makefile_default = os.path.join("src", "MAKE", "Makefile.user_default")
        makefile_user = os.path.join("src", "MAKE", "Makefile.user")
        os.symlink(os.path.basename(makefile_default), makefile_user)
        makefile = FileFilter(makefile_user)
        makefile_auto = FileFilter(os.path.join("src", "MAKE", "Makefile.auto"))

        # Upstream misleadingly suggests that VTK is an optional
        # dependency, but VTK is always needed to create an output file!
        vtk = spec["vtk"]
        makefile.filter(
            r"^#(VTK_INC_USR=-I).*",
            r"\1{0}".format(
                # Glob for the VTK subdirectory like "vtk-8.1".
                glob(os.path.join(vtk.prefix.include, "vtk*"))[0]
            ),
        )
        makefile.filter(r"^#(VTK_LIB_USR=-L).*", r"\1{0}".format(vtk.prefix.lib))

        if spec.satisfies("+mpi"):
            mpi = spec["mpi"]
            makefile.filter(r"^#(MPICXX_USR=).*", r"\1{0}".format(mpi.mpicxx))
            makefile.filter(r"^#(MPI_INC_USR=).*", r"\1{0}".format(mpi.prefix.include))
            makefile.filter(r"^#(MPI_LIB_USR=).*", r"\1{0}".format(mpi.prefix.lib))
        else:
            makefile.filter(r"^(USE_MPI = ).*", r'\1"OFF"')
            # Set path to C++ compiler.
            makefile.filter(r"^#(CXX_USR=).*", r"\1{0}".format(env["CXX"]))

            # Disable compilation sanity check which recursively
            # builds using its own target!
            makefile_auto.filter(r"^(.+)(EXTRA_ADDLIBS.*mpi_stubs.*)", r"\1#\2")

        if spec.satisfies("+jpeg"):
            jpeg = spec["jpeg"]
            makefile.filter(r"^(USE_JPG = ).*", r'\1"ON"')
            makefile.filter(r"^#(JPG_INC_USR=-I).*", r"\1{0}".format(jpeg.prefix.include))
            makefile.filter(r"^#(JPG_LIB_USR=-L).*", r"\1{0}".format(jpeg.prefix.lib))

        if spec.satisfies("+gzip"):
            makefile.filter(r"^(USE_GZIP = ).*", r'\1"ON"')

        if spec.satisfies("+debug"):
            makefile.filter(r"^(USE_DEBUG = ).*", r'\1"ON"')

        if spec.satisfies("+profile"):
            makefile.filter(r"^(USE_PROFILE = ).*", r'\1"ON"')

        # Enable debug output of Makefile.auto in the log file
        # src/Obj_auto/make_auto.log to quickly troubleshoot if
        # anything goes wrong.
        env["AUTO_DEBUG"] = "1"

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(os.path.join("src", "lmp_auto"), prefix.bin.liggghts)
