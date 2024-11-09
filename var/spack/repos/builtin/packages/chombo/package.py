# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Chombo(MakefilePackage):
    """The Chombo package provides a set of tools for implementing finite
    difference and finite-volume methods for the solution of partial
    differential equations on block-structured adaptively refined
    logically rectangular (i.e. Cartesian) grids."""

    homepage = "https://commons.lbl.gov/display/chombo"
    git = "https://bitbucket.org/drhansj/chombo-xsdk.git"

    tags = ["ecp", "ecp-apps"]

    license("BSD-3-Clause-LBNL")

    # Use whatever path Brian V. and Terry L. agreed upon, but preserve version
    version("3.2", commit="71d856c2f469e96755a606db1e5151067da0f54a")
    version("develop", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI parallel support")
    variant("hdf5", default=True, description="Enable HDF5 support")
    variant(
        "dims",
        default="3",
        values=("1", "2", "3", "4", "5", "6"),
        multi=False,
        description="Number of PDE dimensions [1-6]",
    )

    patch("hdf5-16api.patch", when="@3.2", level=0)
    patch("Make.defs.local.template.patch", when="@3.2", level=0)

    depends_on("blas")
    depends_on("lapack")
    depends_on("gmake", type="build")
    depends_on("tcsh", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5", when="+hdf5")
    depends_on("hdf5+mpi", when="+mpi+hdf5")

    def edit(self, spec, prefix):
        files = glob.glob("lib/mk/local/*.csh")
        files += ["fixIncludes", "lib/mk/Make.rules", "lib/mk/reverse"]
        files += ["lib/test/BoxTools/mpirun.sh"]
        filter_file("/bin/csh", "env csh", *files)

        # Set fortran name mangling in Make.defs
        defs_file = FileFilter("./lib/mk/Make.defs")
        defs_file.filter(r"^#\s*cppcallsfort\s*=.*", "cppcallsfort = -DCH_FORT_UNDERSCORE")

        # Set remaining variables in Make.defs.local
        # Make.defs.local.template.patch ensures lines for USE_TIMER,
        # USE_LAPACK and lapackincflags are present
        copy("./lib/mk/Make.defs.local.template", "./lib/mk/Make.defs.local")

        defs_file = FileFilter("./lib/mk/Make.defs.local")

        # Unconditional settings
        defs_file.filter(r"^#\s*DEBUG\s*=.*", "DEBUG = FALSE")
        defs_file.filter(r"^#\s*OPT\s*=.*", "OPT = TRUE")
        # timer code frequently fails compiles. So disable it.
        defs_file.filter(r"^#\s*USE_TIMER\s*=.*", "USE_TIMER = FALSE")

        # LAPACK setup
        lapack_blas = spec["lapack"].libs + spec["blas"].libs
        defs_file.filter(r"^#\s*USE_LAPACK\s*=.*", "USE_LAPACK = TRUE")
        defs_file.filter(
            r"^#\s*lapackincflags\s*=.*", "lapackincflags = -I%s" % spec["lapack"].prefix.include
        )
        defs_file.filter(r"^#\s*syslibflags\s*=.*", "syslibflags = %s" % lapack_blas.ld_flags)

        # Compilers and Compiler flags
        defs_file.filter(r"^#\s*CXX\s*=.*", "CXX = %s" % spack_cxx)
        defs_file.filter(r"^#\s*FC\s*=.*", "FC = %s" % spack_fc)
        if spec.satisfies("+mpi"):
            defs_file.filter(r"^#\s*MPICXX\s*=.*", "MPICXX = %s" % self.spec["mpi"].mpicxx)

        # Conditionally determined settings
        defs_file.filter(r"^#\s*MPI\s*=.*", "MPI = %s" % ("TRUE" if "+mpi" in spec else "FALSE"))
        defs_file.filter(r"^#\s*DIM\s*=.*", "DIM = %s" % spec.variants["dims"].value)

        # HDF5 settings
        if spec.satisfies("+hdf5"):
            defs_file.filter(r"^#\s*USE_HDF5\s*=.*", "USE_HDF5 = TRUE")
            defs_file.filter(
                r"^#\s*HDFINCFLAGS\s*=.*", "HDFINCFLAGS = -I%s" % spec["hdf5"].prefix.include
            )
            defs_file.filter(
                r"^#\s*HDFLIBFLAGS\s*=.*", "HDFLIBFLAGS = %s" % spec["hdf5"].libs.ld_flags
            )
            if spec.satisfies("+mpi"):
                defs_file.filter(
                    r"^#\s*HDFMPIINCFLAGS\s*=.*",
                    "HDFMPIINCFLAGS = -I%s" % spec["hdf5"].prefix.include,
                )
                defs_file.filter(
                    r"^#\s*HDFMPILIBFLAGS\s*=.*",
                    "HDFMPILIBFLAGS = %s" % spec["hdf5"].libs.ld_flags,
                )

    def build(self, spec, prefix):
        with working_dir("lib"):
            make("all")

    def install(self, spec, prefix):
        with working_dir("lib"):
            install_tree("include", prefix.include)
            # The package only builds static libs on Linux,
            # maybe it builds shared libs on another OS.
            # This restores the originally impemented install:
            libfiles = glob.glob("lib*.a")
            libfiles += glob.glob("lib*.so")
            libfiles += glob.glob("lib*.dylib")
            mkdirp(prefix.lib)
            for lib in libfiles:
                install(lib, prefix.lib)
