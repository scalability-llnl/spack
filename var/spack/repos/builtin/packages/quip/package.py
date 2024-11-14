# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess

from spack.package import *


class Quip(MakefilePackage):
    """QUIP - QUantum mechanics and Interatomic Potentials

    The QUIP package is a collection of software tools to carry out molecular
    dynamics simulations. It implements a variety of interatomic potentials and
    tight binding quantum mechanics. It can also call external packages or
    serve as a plugin to packages such as LAMMPS, CP2K and the ASE Python
    framework.
    """

    homepage = "https://libatoms.github.io/QUIP/"
    url = "https://github.com/libAtoms/QUIP/archive/refs/tags/v0.9.14.tar.gz"
    git = "https://github.com/libAtoms/QUIP.git"

    # This package is a Fortran 95 package. It has hidden dependencies
    # through the Fortran module files. Therefore running make in parallel
    # will fail.
    parallel = False

    maintainers("hjjvandam")

    license("GPL-2.0-only", checked_by="hjjvandam")

    # We need to clone the GitHub repo for this library as the Makefile
    # infrastructure tries to use `git` commands while building the code.
    # Downloaded tar-balls are not `git` repos so building from those
    # will fail.
    version(
        "0.9.14",
        # sha256="b6c11c5199e8ba342ea138298fdc99b3861ccd7b9bf048dd95a1e8c125958e12",
        commit="72aaf3fbc9403fe22361bf3fdb4295c516dd1094",
        submodules=True,
    )

    depends_on("fortran", type="build")

    depends_on("blas")
    depends_on("netlib-lapack")

    def setup_build_environment(self, env):
        """Set build environment variables based on the spec

        QUIP requires the selection of an architecture based on
        - the operating system
        - the processor
        - the compiler
        Here we try to guess the right architecture.
        """
        compiler = "gfortran"
        host_os = "linux"
        arch = "x86_64"
        netcdf = "0"
        if self.spec.satisfies("+intel"):
            compiler = "ifort"
        if self.spec.platform == "darwin":
            host_os = "darwin"
        if self.spec.satisfies("+netcdf"):
            netcdf = "1"
        quip_arch = f"{host_os}_{arch}_{compiler}"
        blas = self.spec["blas"].libs.ld_flags
        lapack = self.spec["lapack"].libs.ld_flags
        env.set("GIT_VERSION", str(self.version))
        env.set("QUIP_ARCH", quip_arch)
        env.set("QUIP_ROOT", self.build_directory)
        env.set("QUIP_INSTALLDIR", self.prefix)
        # Spack already set CC, CXX, F77, and FC
        env.set("F77", spack_f77)
        env.set("F90", spack_fc)
        env.set("F95", spack_fc)
        env.set("CPLUSPLUS", spack_cxx)
        env.set("MATH_LINKOPTS", f"{lapack} {blas}")
        env.set("EXTRA_LINKOPTS", " ")
        env.set("HAVE_CP2K", "1")
        env.set("HAVE_VASP", "1")
        env.set("HAVE_TB", "1")
        env.set("HAVE_PRECON", "0")
        env.set("HAVE_LOFT", "0")
        env.set("HAVE_ONIOM", "1")
        env.set("HAVE_LOCAL_E_MIX", "1")
        env.set("HAVE_QC", "1")
        env.set("HAVE_GAP", "0")
        env.set("HAVE_QR", "0")
        env.set("HAVE_SCALAPACK", "0")
        env.set("HAVE_FX", "0")
        env.set("HAVE_SCME", "0")
        env.set("HAVE_MTP", "0")
        env.set("HAVE_MBD", "0")
        env.set("HAVE_TTM_NF", "0")
        env.set("HAVE_CH4", "0")
        env.set("HAVE_NETCDF4", netcdf)
        env.set("HAVE_MDCORE", "0")
        env.set("HAVE_ASAP", "0")
        env.set("HAVE_CGAL", "0")
        env.set("HAVE_METIS", "0")
        env.set("HAVE_LMTO_TBE", "0")

    def edit(self, spec, prefix):
        #
        # Hack the GIT_VERSION setting in Makefile.rules. The gitversion tool
        # that Makefile.rules uses by default is not reliably available.
        gitversion = self.version
        makefile = FileFilter(join_path(self.build_directory, "Makefile.rules"))
        makefile.filter(
            r"^\s*GIT_VERSION\s*:=.*", f"GIT_VERSION := -D'GIT_VERSION=\"{gitversion}\"'"
        )
        #
        # Makefile.config requires user input when writing Makefile.inc.
        # Obviously in an automated environment like Spack we cannot
        # rely on user input. Therefore we write Makefile.inc ourselves.
        quip_arch = os.environ["QUIP_ARCH"]
        make_dir = join_path(self.build_directory, "build", quip_arch)
        make_inc = join_path(make_dir, "Makefile.inc")
        os.makedirs(make_dir, exist_ok=True)
        list_vars = [
            "QUIP_ARCH",
            "QUIP_ROOT",
            "QUIP_INSTALLDIR",
            "F77",
            "F90",
            "F95",
            "CPLUSPLUS",
            "MATH_LINKOPTS",
            "EXTRA_LINKOPTS",
            "HAVE_CP2K",
            "HAVE_VASP",
            "HAVE_TB",
            "HAVE_PRECON",
            "HAVE_LOFT",
            "HAVE_ONIOM",
            "HAVE_LOCAL_E_MIX",
            "HAVE_QC",
            "HAVE_GAP",
            "HAVE_QR",
            "HAVE_SCALAPACK",
            "HAVE_FX",
            "HAVE_SCME",
            "HAVE_MTP",
            "HAVE_MBD",
            "HAVE_TTM_NF",
            "HAVE_CH4",
            "HAVE_NETCDF4",
            "HAVE_MDCORE",
            "HAVE_ASAP",
            "HAVE_CGAL",
            "HAVE_METIS",
            "HAVE_LMTO_TBE",
        ]
        quip_root = os.environ["QUIP_ROOT"]
        sizeof = join_path(quip_root, "bin", "find_sizeof_fortran_t")
        with open(make_inc, "w") as fp:
            fp.write(f"GIT_VERSION = \"{os.environ['GIT_VERSION']}\"\n")
            for key in list_vars:
                fp.write(f"{key} = {os.environ[key]}\n")
        # Append SIZEOF_FORTRAN_T setting (without the next open statement
        # the setting is prepended to Makefile.inc(?))
        with open(make_inc, "a") as fp:
            subprocess.run(["bash", sizeof], stdout=fp, check=True)

    def build(self, spec, prefix):
        #
        # Note that os.chdir does not change PWD in the Python process
        # so make will inherit the old PWD from Python. This causes
        # problems when Makefile calls make for the fox library.
        # To avoid that we need to update PWD explicitly. Just to make things
        # more interesting os.getcwd does return the current working directory
        # as it is after os.chdir.
        os.chdir(self.build_directory)
        build_path = os.getcwd()
        os.environ["PWD"] = build_path
        #
        # With the correct environment we can call make.
        make()

    def install(self, spec, prefix):
        make("install")
