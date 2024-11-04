# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re

from spack.package import *


class SpectrumMpi(BundlePackage):
    """IBM MPI implementation from Spectrum MPI."""

    has_code = False

    homepage = "https://www-03.ibm.com/systems/spectrum-computing/products/mpi"

    # https://www.ibm.com/docs/en/smpi/10.4
    version("10.4")

    provides("mpi")

    requires("platform=linux")

    executables = ["^ompi_info$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r"Spectrum MPI: (\S+)", output)
        if not match:
            return None
        version = match.group(1)
        return version

    @classmethod
    def determine_variants(cls, exes, version):
        compiler_suites = {
            "xl": {"cc": "mpixlc", "cxx": "mpixlC", "f77": "mpixlf", "fc": "mpixlf"},
            "pgi": {"cc": "mpipgicc", "cxx": "mpipgic++", "f77": "mpipgifort", "fc": "mpipgifort"},
            "default": {"cc": "mpicc", "cxx": "mpicxx", "f77": "mpif77", "fc": "mpif90"},
        }

        def get_host_compiler(exe):
            output = Executable(exe)("--showme", output=str, error=str)
            match = re.search(r"^(\S+)", output)
            return match.group(1) if match else None

        def get_spack_compiler_spec(compilers_found):
            # check using cc for now, as everyone should have that defined.
            path = os.path.dirname(compilers_found["cc"])
            spack_compilers = spack.compilers.find_compilers([path])
            actual_compiler = None
            # check if the compiler actually matches the one we want
            for spack_compiler in spack_compilers:
                if os.path.dirname(spack_compiler.cc) == path:
                    actual_compiler = spack_compiler
                    break
            return actual_compiler.spec if actual_compiler else None

        def get_opal_prefix(exe):
            output = Executable(exe)(output=str, error=str)
            match = re.search(r"Prefix: (\S+)", output)
            if not match:
                return None
            opal_prefix = match.group(1)
            return opal_prefix

        results = []
        for exe in exes:
            dirname = os.path.dirname(exe)
            siblings = os.listdir(dirname)
            compilers_found = {}
            for compiler_suite in compiler_suites.values():
                for compiler_class, compiler_name in compiler_suite.items():
                    if compiler_name in siblings:
                        # Get the real name of the compiler
                        full_exe = os.path.join(dirname, compiler_name)
                        host_exe = get_host_compiler(full_exe)
                        if host_exe:
                            compilers_found[compiler_class] = host_exe
                if compilers_found:
                    break
            if compilers_found:
                compiler_spec = get_spack_compiler_spec(compilers_found)
                if compiler_spec:
                    variant = "%" + str(compiler_spec)
                else:
                    variant = ""
                # Use this variant when you need to define the
                # compilers explicitly
                #
                # results.append((variant, {'compilers': compilers_found}))
                #
                # Otherwise, use this simpler attribute
            else:
                variant = ""
            opal_prefix = get_opal_prefix(exe)
            if opal_prefix:
                extra_attributes = {"opal_prefix": opal_prefix}
                results.append((variant, extra_attributes))
            else:
                results.append(variant)
        return results

    def setup_dependent_package(self, module, dependent_spec):
        # get the compiler names
        if "%xl" in dependent_spec or "%xl_r" in dependent_spec:
            self.spec.mpicc = os.path.join(self.prefix.bin, "mpixlc")
            self.spec.mpicxx = os.path.join(self.prefix.bin, "mpixlC")
            self.spec.mpif77 = os.path.join(self.prefix.bin, "mpixlf")
            self.spec.mpifc = os.path.join(self.prefix.bin, "mpixlf")
        elif "%pgi" in dependent_spec:
            self.spec.mpicc = os.path.join(self.prefix.bin, "mpipgicc")
            self.spec.mpicxx = os.path.join(self.prefix.bin, "mpipgic++")
            self.spec.mpif77 = os.path.join(self.prefix.bin, "mpipgifort")
            self.spec.mpifc = os.path.join(self.prefix.bin, "mpipgifort")
        else:
            self.spec.mpicc = os.path.join(self.prefix.bin, "mpicc")
            self.spec.mpicxx = os.path.join(self.prefix.bin, "mpicxx")
            self.spec.mpif77 = os.path.join(self.prefix.bin, "mpif77")
            self.spec.mpifc = os.path.join(self.prefix.bin, "mpif90")

    def setup_dependent_build_environment(self, env, dependent_spec):
        if "%xl" in dependent_spec or "%xl_r" in dependent_spec:
            env.set("MPICC", os.path.join(self.prefix.bin, "mpixlc"))
            env.set("MPICXX", os.path.join(self.prefix.bin, "mpixlC"))
            env.set("MPIF77", os.path.join(self.prefix.bin, "mpixlf"))
            env.set("MPIF90", os.path.join(self.prefix.bin, "mpixlf"))
        elif "%pgi" in dependent_spec:
            env.set("MPICC", os.path.join(self.prefix.bin, "mpipgicc"))
            env.set("MPICXX", os.path.join(self.prefix.bin, "mpipgic++"))
            env.set("MPIF77", os.path.join(self.prefix.bin, "mpipgifort"))
            env.set("MPIF90", os.path.join(self.prefix.bin, "mpipgifort"))
        else:
            env.set("MPICC", os.path.join(self.prefix.bin, "mpicc"))
            env.set("MPICXX", os.path.join(self.prefix.bin, "mpic++"))
            env.set("MPIF77", os.path.join(self.prefix.bin, "mpif77"))
            env.set("MPIF90", os.path.join(self.prefix.bin, "mpif90"))

        dependent_module = dependent_spec.package.module
        env.set("OMPI_CC", dependent_module.spack_cc)
        env.set("OMPI_CXX", dependent_module.spack_cxx)
        env.set("OMPI_FC", dependent_module.spack_fc)
        env.set("OMPI_F77", dependent_module.spack_f77)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)

    def setup_run_environment(self, env):
        # Because MPI functions as a compiler we need to setup the compilers
        # in the run environment, like any compiler
        if "%xl" in self.spec or "%xl_r" in self.spec:
            env.set("MPICC", os.path.join(self.prefix.bin, "mpixlc"))
            env.set("MPICXX", os.path.join(self.prefix.bin, "mpixlC"))
            env.set("MPIF77", os.path.join(self.prefix.bin, "mpixlf"))
            env.set("MPIF90", os.path.join(self.prefix.bin, "mpixlf"))
        elif "%pgi" in self.spec:
            env.set("MPICC", os.path.join(self.prefix.bin, "mpipgicc"))
            env.set("MPICXX", os.path.join(self.prefix.bin, "mpipgic++"))
            env.set("MPIF77", os.path.join(self.prefix.bin, "mpipgifort"))
            env.set("MPIF90", os.path.join(self.prefix.bin, "mpipgifort"))
        else:
            env.set("MPICC", os.path.join(self.prefix.bin, "mpicc"))
            env.set("MPICXX", os.path.join(self.prefix.bin, "mpic++"))
            env.set("MPIF77", os.path.join(self.prefix.bin, "mpif77"))
            env.set("MPIF90", os.path.join(self.prefix.bin, "mpif90"))

        env.set("OPAL_PREFIX", self.spec.extra_attributes.get("opal_prefix", self.prefix))
        env.set("MPI_ROOT", self.spec.extra_attributes.get("opal_prefix", self.prefix))
