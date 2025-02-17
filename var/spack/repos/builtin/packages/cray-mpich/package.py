# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *
from spack.pkg.builtin.mpich import MpichEnvironmentModifications
from spack.util.module_cmd import get_path_args_from_module_line, module


class CrayMpich(MpichEnvironmentModifications, Package, CudaPackage, ROCmPackage):
    """Cray's MPICH is a high performance and widely portable implementation of
    the Message Passing Interface (MPI) standard."""

    homepage = "https://docs.nersc.gov/development/compilers/wrappers/"
    has_code = False  # Skip attempts to fetch source that is not available

    maintainers("etiennemlb", "haampie")

    version("8.1.30")
    version("8.1.28")
    version("8.1.25")
    version("8.1.24")
    version("8.1.21")
    version("8.1.14")
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
            self.setup_mpi_wrapper_variables(env)
            return

        env.set("MPICC", self.compiler.cc)
        env.set("MPICXX", self.compiler.cxx)
        env.set("MPIFC", self.compiler.fc)
        env.set("MPIF77", self.compiler.f77)

    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec
        if spec.satisfies("+wrappers"):
            MpichEnvironmentModifications.setup_dependent_package(self, module, dependent_spec)
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

    @property
    def gtl_lib(self):
        # GPU transport Layer (GTL) handling background:
        # - The cray-mpich module defines an environment variable per supported
        # GPU (say, PE_MPICH_GTL_LIBS_amd_gfx942). So we should read the
        # appropriate variable.
        # In practice loading a module and checking its content is a PITA. We
        # simplify by assuming that the GTL for a given vendor (say, AMD), is
        # one and the same for all the targets of this vendor (one GTL for all
        # Nvidia or one GTL for all AMD devices).
        # - Second, except if you have a very weird mpich layout, the GTL are
        # located in /opt/cray/pe/mpich/<cray_mpich_version>/gtl/lib when the
        # MPI libraries are in
        # /opt/cray/pe/mpich/<cray_mpich_version>/ofi/<vendor>/<vendor_version>.
        # Example:
        #   /opt/cray/pe/mpich/8.1.28/gtl/lib
        #   /opt/cray/pe/mpich/8.1.28/ofi/<vendor>/<vendor_version>
        #   /opt/cray/pe/mpich/8.1.28/ofi/<vendor>/<vendor_version>/../../../gtl/lib

        gtl_kinds = {
            "cuda": {
                "lib": "libmpi_gtl_cuda",
                "variant": "cuda_arch",
                "values": {"70", "80", "90"},
            },
            "rocm": {
                "lib": "libmpi_gtl_hsa",
                "variant": "amdgpu_target",
                "values": {"gfx906", "gfx908", "gfx90a", "gfx940", "gfx942"},
            },
        }

        for variant, gtl_kind in gtl_kinds.items():
            arch_variant = gtl_kind["variant"]
            arch_values = gtl_kind["values"]
            gtl_lib = gtl_kind["lib"]

            if self.spec.satisfies(f"+{variant} {arch_variant}=*"):
                accelerator_architecture_set = set(self.spec.variants[arch_variant].value)

                if len(
                    accelerator_architecture_set
                ) >= 1 and not accelerator_architecture_set.issubset(arch_values):
                    raise InstallError(
                        f"cray-mpich variant '+{variant} {arch_variant}'"
                        " was specified but no GTL support could be found for it."
                    )

                mpi_root = os.path.abspath(
                    os.path.join(self.prefix, os.pardir, os.pardir, os.pardir)
                )

                gtl_root = os.path.join(mpi_root, "gtl", "lib")

                gtl_shared_libraries = find_libraries(
                    [gtl_lib], root=gtl_root, shared=True, recursive=False
                )

                if len(gtl_shared_libraries) != 1:
                    raise InstallError(
                        f"cray-mpich variant '+{variant} {arch_variant}'"
                        " was specified and GTL support was found for it but"
                        f" the '{gtl_lib}' could not be correctly found on disk."
                    )

                gtl_library_fullpath = list(gtl_shared_libraries)[0]
                tty.debug(f"Selected GTL: {gtl_library_fullpath}")

                gtl_library_directory = os.path.dirname(gtl_library_fullpath)
                gtl_library_name = os.path.splitext(
                    os.path.basename(gtl_library_fullpath).split("lib")[1]
                )[0]

                # Early break. Only one GTL can be active at a given time.
                return {
                    "ldflags": [
                        f"-L{gtl_library_directory}",
                        f"-Wl,-rpath,{gtl_library_directory}",
                    ],
                    "ldlibs": [f"-l{gtl_library_name}"],
                }
        return {}
