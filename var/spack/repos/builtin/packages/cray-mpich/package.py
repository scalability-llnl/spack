# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.util.module_cmd import get_path_args_from_module_line, module


class CrayMpich(Package):
    """Cray's MPICH is a high performance and widely portable implementation of
    the Message Passing Interface (MPI) standard."""

    homepage = "https://docs.nersc.gov/development/compilers/wrappers/"
    has_code = False  # Skip attempts to fetch source that is not available

    maintainers("haampie")

    version("8.1.7")
    version("8.1.0")
    version("8.0.16")
    version("8.0.14")
    version("8.0.11")
    version("8.0.9")
    version("7.7.16")
    version("7.7.15")
    version("7.7.14")
    version("7.7.13")

    depends_on("cray-pmi")
    depends_on("libfabric")

    requires("platform=linux", msg="Cray MPICH is only available on Cray")

    # cray-mpich 8.1.7: features MPI compiler wrappers
    variant("wrappers", default=True, when="@8.1.7:", description="enable MPI wrappers")

    provides("mpi@3")

    canonical_names = {
        "gcc": "GNU",
        "cce": "CRAY",
        "intel": "INTEL",
        "clang": "ALLINEA",
        "aocc": "AOCC",
    }

    @property
    def modname(self):
        return "cray-mpich/{0}".format(self.version)

    @property
    def external_prefix(self):
        mpich_module = module("show", self.modname).splitlines()

        for line in mpich_module:
            if "CRAY_MPICH_DIR" in line:
                return get_path_args_from_module_line(line)[0]

        # Fixes an issue on Archer2 cray-mpich/8.0.16 where there is
        # no CRAY_MPICH_DIR variable in the module file.
        for line in mpich_module:
            if "CRAY_LD_LIBRARY_PATH" in line:
                libdir = get_path_args_from_module_line(line)[0]
                return os.path.dirname(os.path.normpath(libdir))

    def setup_run_environment(self, env):
        if self.spec.satisfies("+wrappers"):
            env.set("MPICC", join_path(self.prefix.bin, "mpicc"))
            env.set("MPICXX", join_path(self.prefix.bin, "mpicxx"))
            env.set("MPIF77", join_path(self.prefix.bin, "mpif77"))
            env.set("MPIF90", join_path(self.prefix.bin, "mpif90"))
        elif spack_cc is not None:
            env.set("MPICC", spack_cc)
            env.set("MPICXX", spack_cxx)
            env.set("MPIF77", spack_fc)
            env.set("MPIF90", spack_fc)

    def setup_dependent_build_environment(self, env, dependent_spec):
        dependent_module = dependent_spec.package.module
        env.set("MPICH_CC", dependent_module.spack_cc)
        env.set("MPICH_CXX", dependent_module.spack_cxx)
        env.set("MPICH_F77", dependent_module.spack_f77)
        env.set("MPICH_F90", dependent_module.spack_fc)
        env.set("MPICH_FC", dependent_module.spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec
        if spec.satisfies("+wrappers"):
            spec.mpicc = join_path(self.prefix.bin, "mpicc")
            spec.mpicxx = join_path(self.prefix.bin, "mpicxx")
            spec.mpifc = join_path(self.prefix.bin, "mpif90")
            spec.mpif77 = join_path(self.prefix.bin, "mpif77")
        elif spack_cc is not None:
            spec.mpicc = spack_cc
            spec.mpicxx = spack_cxx
            spec.mpifc = spack_fc
            spec.mpif77 = spack_f77

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )

    @property
    def headers(self):
        hdrs = find_headers("mpi", self.prefix.include, recursive=True)
        hdrs.directories = os.path.dirname(hdrs[0])
        return hdrs

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters

        libraries = ["libmpich"]

        if "cxx" in query_parameters:
            libraries.extend(["libmpicxx", "libmpichcxx"])

        if "f77" in query_parameters:
            libraries.extend(["libmpifort", "libmpichfort", "libfmpi", "libfmpich"])

        if "f90" in query_parameters:
            libraries.extend(["libmpif90", "libmpichf90"])

        libs = find_libraries(libraries, root=self.prefix.lib, recursive=True)
        libs += find_libraries(libraries, root=self.prefix.lib64, recursive=True)

        return libs
