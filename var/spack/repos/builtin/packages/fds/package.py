# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fds(MakefilePackage):
    """
    Fire Dynamics Simulator (FDS) is a large-eddy simulation (LES) code for low-speed flows,
    with an emphasis on smoke and heat transport from fires.
    FDS and Smokeview are free and open-source software tools provided by the National Institute
    of Standards and Technology (NIST) of the United States Department of Commerce. Pursuant
    to Title 17, Section 105 of the United States Code, this software is not subject to copyright
    protection and is in the public domain. View the full disclaimer for NIST-developed software.
    """

    maintainers("kjrstory")
    homepage = "https://pages.nist.gov/fds-smv"
    url = "https://github.com/firemodels/fds/archive/refs/tags/FDS-6.8.0.tar.gz"
    git = "https://github.com/firemodels/fds.git"

    version("6.9.1", commit="889da6ae08d08dae680f7c0d8de66a3ad1c65375")
    version("6.9.0", commit="63395692607884566fdedb5db4b5b4d98d3bcafb")
    version("6.8.0", commit="886e0096535519b7358a3c4393c91da3caee5072")

    variant("openmp", default=False, description="Enable OpenMP support")

    conflicts("%gcc", when="+openmp", msg="GCC already provides OpenMP support")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("mkl")

    build_directory = "Build"

    requires(
        "%gcc",
        "%intel",
        "%oneapi",
        policy="one_of",
        msg="FDS builds only with GNU Fortran or Intel Fortran",
    )

    requires(
        "^intel-mkl",
        "^intel-oneapi-mkl",
        policy="one_of",
        msg="FDS builds require either Intel MKL or Intel oneAPI MKL library",
    )

    requires(
        "^openmpi",
        when="%gcc platform=linux",
        msg="OpenMPI can only be used with GNU Fortran on Linux platform",
    )

    requires(
        "^intel-mpi^intel-mkl",
        when="%intel platform=linux",
        msg="Intel MPI and Intel MKL can only be used with Intel Fortran on Linux platform",
    )

    requires(
        "^intel-oneapi-mpi^intel-oneapi-mkl",
        when="%oneapi platform=linux",
        msg="Intel oneAPI MPI and MKL can only be used with oneAPI Fortran on Linux platform",
    )

    requires(
        "^openmpi%intel",
        when="platform=darwin",
        msg="OpenMPI can only be used with Intel Fortran on macOS",
    )

    def edit(self, spec, prefix):
        env["MKL_ROOT"] = self.spec["mkl"].prefix
        if spec.compiler.name == "oneapi":
            env["INTEL_IFORT"] = "ifx"
        makefile = FileFilter("Build/makefile")
        makefile.filter(r"\.\./Scripts", "./Scripts")
        makefile.filter(r"\.\.\\Scripts", ".\\Scripts")

    @property
    def build_targets(self):
        spec = self.spec
        mpi_mapping = {"openmpi": "ompi", "intel-oneapi-mpi": "impi", "intel-mpi": "impi"}
        compiler_mapping = {"gcc": "gnu", "oneapi": "intel", "intel": "intel"}
        platform_mapping = {"linux": "linux", "darwin": "osx"}
        mpi_prefix = mpi_mapping[spec["mpi"].name]
        compiler_prefix = compiler_mapping[spec.compiler.name]
        platform_prefix = platform_mapping[spec.architecture.platform]
        openmp_prefix = "_openmp" if "+openmp" in spec else ""
        return [f"{mpi_prefix}_{compiler_prefix}_{platform_prefix}{openmp_prefix}"]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("*.mod", prefix.bin)
            install("*.o", prefix.bin)
            install("fds_" + self.build_targets[0], join_path(prefix.bin, "fds"))
