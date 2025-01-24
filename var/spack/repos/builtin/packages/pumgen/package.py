# Copyright 2013-2025 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pumgen(CMakePackage):
    """PUMGen - A mesh converter to the PUML format, as used in SeisSol."""

    homepage = "https://github.com/SeisSol/PUMGen/wiki/How-to-compile-PUMGen"
    git = "https://github.com/SeisSol/PUMGen.git"
    version("master", branch="master", submodules=True)

    version(
        "1.1.1", tag="v1.1.1", commit="ad3d0f22edfdb72713ef7bb42a41251fa7275bd8", submodules=True
    )
    version(
        "1.0.1", tag="v1.0.1", commit="13d1e1f41e3cdcb1d3c94f1870f003778e5f0ce0", submodules=True
    )
    maintainers("Thomas-Ulrich", "davschneller", "vikaskurapati")
    variant(
        "with_simmetrix",
        default=False,
        description="Use Simmetrix libraries, embedding mesh generation with Simmetrix in PUMGen",
    )
    variant(
        "scorec",
        default=False,
        description="Use PUMI (Parallel Unstructured Mesh Infrastructure) Scorec, \
            instead of standalone PUMGen functions.",
    )
    variant("with_netcdf", default=False, description="Support netcdf meshes")

    depends_on("mpi")
    # simmetrix (e.g. @2024.0-240616) currently does not
    # have a precompiled libSimPartitionWrapper-openmpi5.a
    depends_on("openmpi@:4", when="+with_simmetrix ^[virtuals=mpi] openmpi")

    depends_on(
        "netcdf-c +shared +mpi", when="+with_netcdf"
    )  # NOTE: only tested with 4.4.0 version
    depends_on("hdf5@1.10: +shared +threadsafe +mpi")
    depends_on("simmetrix-simmodsuite", when="+with_simmetrix")
    depends_on(
        "pumi +int64 simmodsuite=base +zoltan ~fortran ~simmodsuite_version_check",
        when="+with_simmetrix +scorec",
    )
    with when("@1.0.1"):
        depends_on("pumi +int64 +zoltan ~fortran", when="~with_simmetrix")
        depends_on(
            "pumi +int64 simmodsuite=base +zoltan ~fortran ~simmodsuite_version_check",
            when="+with_simmetrix",
        )

    depends_on("zoltan@3.83 +parmetis+int64 ~fortran +shared")
    depends_on("easi@1.2: +asagi jit=impalajit,lua", when="+with_simmetrix")

    def cmake_args(self):
        args = [
            self.define_from_variant("SIMMETRIX", "with_simmetrix"),
            self.define_from_variant("NETCDF", "with_netcdf"),
            self.define_from_variant("SCOREC", "scorec"),
        ]
        if "simmetrix-simmodsuite" in self.spec:
            mpi_id = self.spec["mpi"].name + self.spec["mpi"].version.up_to(1).string
            args.append("-DSIM_MPI=" + mpi_id)
            args.append("-DSIMMETRIX_ROOT=" + self.spec["simmetrix-simmodsuite"].prefix)
        return args

    def install(self, spec, prefix):
        self.cmake(spec, prefix)
        self.build(spec, prefix)
        install_tree(self.build_directory, prefix.bin)
