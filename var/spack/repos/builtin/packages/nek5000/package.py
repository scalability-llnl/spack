# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from shutil import copyfile

from spack.package import *


class Nek5000(Package):
    """A fast and scalable high-order solver for computational fluid
    dynamics"""

    homepage = "https://nek5000.mcs.anl.gov/"
    url = "https://github.com/Nek5000/Nek5000/archive/v17.0.tar.gz"
    git = "https://github.com/Nek5000/Nek5000.git"

    tags = [
        "cfd",
        "flow",
        "hpc",
        "solver",
        "navier-stokes",
        "spectral-elements",
        "fluid",
        "ecp",
        "ecp-apps",
    ]

    version("develop", branch="master")
    version("17.0", sha256="4d8d4793ce3c926c54e09a5a5968fa959fe0ba46bd2e6b8043e099528ee35a60")
    version("19.0", sha256="db129877a10ff568d49edc77cf65f9e732eecb1fce10edbd91ffc5ac10c41ad6")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # MPI, Profiling and Visit variants
    variant("mpi", default=True, description="Build with MPI.")
    variant("profiling", default=True, description="Build with profiling data.")
    variant("visit", default=False, description="Build with Visit.")

    # TODO: add a variant 'blas' or 'external-blas' to enable the usage of
    #       Spack installed/configured blas.

    # Dependencies
    depends_on("mpi", when="+mpi")

    patch("add_fjfortran.patch", when="%fj")

    @run_before("install")
    def fortran_check(self):
        if not self.compiler.f77:
            msg = "Cannot build Nek5000 without a Fortran 77 compiler."
            raise RuntimeError(msg)

    @run_after("install")
    def check_install(self):
        with working_dir("short_tests/eddy"):
            f_size = join_path(os.getcwd(), "SIZE")
            f_size_legacy = join_path(os.getcwd(), "SIZE.legacy")
            if not os.access(f_size, os.F_OK):
                if os.access(f_size_legacy, os.F_OK):
                    copyfile(f_size_legacy, f_size)
                else:
                    raise RuntimeError("Can not find {0}".format(f_size))

            os.system(join_path(self.prefix.bin, "makenek") + " eddy_uv")
            if not os.path.isfile(join_path(os.getcwd(), "nek5000")):
                msg = "Cannot build example: short_tests/eddy."
                raise RuntimeError(msg)

    def install(self, spec, prefix):
        bin_dir = "bin"

        # Do not use the Spack compiler wrappers.
        # Use directly the compilers:
        fc = self.compiler.f77
        cc = self.compiler.cc

        fflags = spec.compiler_flags["fflags"]
        cflags = spec.compiler_flags["cflags"]

        if self.compiler.name in ["xl", "xl_r"]:
            # Use '-qextname' to add underscores.
            # Use '-WF,-qnotrigraph' to fix an error about a string: '... ??'
            fflags += ["-qextname", "-WF,-qnotrigraph"]

        error = Executable(fc)("empty.f", output=str, error=str, fail_on_error=False)

        if "gfortran" in error or "GNU" in error or "gfortran" in fc:
            # Use '-std=legacy' to suppress an error that used to be a
            # warning in previous versions of gfortran.
            fflags += ["-std=legacy"]

        fflags = " ".join(fflags)
        cflags = " ".join(cflags)

        with working_dir(bin_dir):
            if "+mpi" in spec:
                fc = spec["mpi"].mpif77
                cc = spec["mpi"].mpicc
            else:
                filter_file(r"^#MPI=0", "MPI=0", "makenek")

            # Make sure nekmpi wrapper uses srun when we know OpenMPI
            # is not built with mpiexec
            if "^openmpi~legacylaunchers" in spec:
                filter_file(r"mpiexec -np", "srun -n", "nekmpi")

            if "+profiling" not in spec:
                filter_file(r"^#PROFILING=0", "PROFILING=0", "makenek")

            if "+visit" in spec:
                filter_file(r"^#VISIT=1", "VISIT=1", "makenek")
                filter_file(
                    r"^#VISIT_INSTALL=.*",
                    'VISIT_INSTALL="' + spec["visit"].prefix.bin + '"',
                    "makenek",
                )

            # Update the makenek to use correct compilers and
            # Nek5000 source.
            filter_file(r"^#FC\s*=.*", 'FC="{0}"'.format(fc), "makenek")
            filter_file(r"^#CC\s*=.*", 'CC="{0}"'.format(cc), "makenek")
            if self.spec.version == Version("17.0"):
                filter_file(
                    r"^#SOURCE_ROOT\s*=\"\$H.*",
                    'SOURCE_ROOT="' + prefix.bin.Nek5000 + '"',
                    "makenek",
                )
            else:
                filter_file(
                    r"^#NEK_SOURCE_ROOT\s*=\"\$H.*",
                    'NEK_SOURCE_ROOT="' + prefix.bin.Nek5000 + '"',
                    "makenek",
                )

            if fflags:
                filter_file(r"^#FFLAGS=.*", 'FFLAGS+=" {0}"'.format(fflags), "makenek")
            if cflags:
                filter_file(r"^#CFLAGS=.*", 'CFLAGS+=" {0}"'.format(cflags), "makenek")

        with working_dir("core"):
            if self.compiler.name in ["xl", "xl_r"]:
                # Patch 'core/makenek.inc' and 'makefile.template' to use
                # '-qextname' when checking for underscore becasue 'xl'/'xl_r'
                # use this option to enable the addition of the underscore.
                filter_file(r"^\$FCcomp -c ", "$FCcomp -qextname -c ", "makenek.inc")
                filter_file(
                    r"\$\(FC\) -c \$\(L0\)", "$(FC) -c -qextname $(L0)", "makefile.template"
                )

        # Install Nek5000/bin in prefix/bin
        install_tree(bin_dir, prefix.bin)

        # Copy Nek5000 source to prefix/bin
        install_tree(self.stage.source_path, prefix.bin.Nek5000)
