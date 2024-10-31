# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os

from spack.package import *


class Nekcem(Package):
    """Spectral-element solver for Maxwell's equations, drift-diffusion
    equations, and more."""

    # Links to homepage and git
    homepage = "https://nekcem.mcs.anl.gov"
    git = "https://github.com/NekCEM/NekCEM.git"

    # Variants
    variant("mpi", default=True, description="Build with MPI")

    # We only have a development version
    version("develop", branch="development")
    # The following hash-versions are used by the 'ceed' package
    version("c8db04b", commit="c8db04b96f9b9cb0434ee75da711502fe95891b5")
    version("0b8bedd", commit="0b8beddfdcca646bfcc866dfda1c5f893338399b")
    version("7332619", commit="7332619b73d03868a256614b61794dce2d95b360")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # dependencies
    depends_on("mpi", when="+mpi")
    depends_on("blas")
    depends_on("lapack")

    @run_before("install")
    def fortran_check(self):
        if not self.compiler.fc:
            msg = "NekCEM can not be built without a Fortran compiler."
            raise RuntimeError(msg)

    @run_after("install")
    def check_install(self):
        nekcem_test = join_path(self.prefix.bin, "NekCEM", "tests", "2dboxpec")
        with working_dir(nekcem_test):
            makenek = Executable(join_path(self.prefix.bin, "makenek"))
            makenek(os.path.basename(nekcem_test))
            if not os.path.isfile("nekcem"):
                msg = "Cannot build example: %s" % nekcem_test
                raise RuntimeError(msg)

    def install(self, spec, prefix):
        bin_dir = "bin"
        nek = "nek"
        configurenek = "configurenek"
        makenek = "makenek"

        fc = self.compiler.f77
        cc = self.compiler.cc

        fflags = spec.compiler_flags["fflags"]
        cflags = spec.compiler_flags["cflags"]
        ldflags = spec.compiler_flags["ldflags"]

        if "+mpi" in spec:
            fc = spec["mpi"].mpif77
            cc = spec["mpi"].mpicc

        with working_dir(bin_dir):
            fflags = ["-O3"] + fflags
            cflags = ["-O3"] + cflags
            fflags += ["-I."]
            cflags += ["-I.", "-DGLOBAL_LONG_LONG"]

            if self.compiler.name == "gcc" or self.compiler.name == "clang":
                # assuming 'clang' uses 'gfortran'
                fflags += ["-fdefault-real-8", "-fdefault-double-8"]
                cflags += ["-DUNDERSCORE"]
            elif self.compiler.name == "intel":
                fflags += ["-r8"]
                cflags += ["-DUNDERSCORE"]
            elif self.compiler.name == "xl" or self.compiler.name == "xl_r":
                fflags += ["-qrealsize=8"]
                cflags += ["-DPREFIX=jl_", "-DIBM"]
            elif self.compiler.name == "pgi":
                fflags += ["-r8"]
                cflags += ["-DUNDERSCORE"]

            error = Executable(fc)("empty.f", output=str, error=str, fail_on_error=False)

            if "gfortran" in error or "GNU" in error or "gfortran" in fc:
                # Use '-std=legacy' to suppress an error that used to be a
                # warning in previous versions of gfortran.
                fflags += ["-std=legacy"]

            if "+mpi" in spec:
                fflags += ["-DMPI", "-DMPIIO"]
                cflags += ["-DMPI", "-DMPIIO"]
            blas_lapack = spec["lapack"].libs + spec["blas"].libs
            pthread_lib = find_system_libraries("libpthread")
            ldflags += (blas_lapack + pthread_lib).ld_flags.split()
            all_arch = {
                "spack-arch": {
                    "FC": fc,
                    "FFLAGS": fflags,
                    "CC": cc,
                    "CFLAGS": cflags,
                    "LD": fc,
                    "LDFLAGS": ldflags,
                }
            }
            os.rename("arch.json", "arch.json.orig")
            with open("arch.json", "w") as file:
                file.write(json.dumps(all_arch))
            filter_file(r"^ARCH=.*$", "ARCH=spack-arch", "makenek")
            filter_file(r"^NEK=.*", 'NEK="%s"' % prefix.bin.NekCEM, "makenek")

        # Install NekCEM in prefix/bin
        install_tree(self.stage.source_path, prefix.bin.NekCEM)
        # Create symlinks to makenek, nek and configurenek scripts
        with working_dir(prefix.bin):
            os.symlink(os.path.join("NekCEM", bin_dir, makenek), makenek)
            os.symlink(os.path.join("NekCEM", bin_dir, configurenek), configurenek)
            os.symlink(os.path.join("NekCEM", bin_dir, nek), nek)
