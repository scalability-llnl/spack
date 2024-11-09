# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *
from spack.util.executable import Executable


class MpasModel(MakefilePackage):
    """The Model for Prediction Across Scales (MPAS) is a collaborative
    project for developing atmosphere, ocean and other earth-system
    simulation components for use in climate, regional climate and weather
    studies."""

    homepage = "https://mpas-dev.github.io/"
    url = "https://github.com/MPAS-Dev/MPAS-Model/archive/v7.0.tar.gz"
    maintainers("t-brown")

    version("7.3", sha256="a6a9570911b47aa3607036c1ab5a9ae770f9f3a85cea2710f08bb3b35c08facf")
    version("7.2", sha256="3158c22e4a33ae00ce20b65f6ad189c0b7839587dee124d685b02f9df9cf27a7")
    version("7.1", sha256="9b5c181b7d0163ae33d24d7a79ede6990495134b58cf4500ba5c8c94192102bc")
    version("7.0", sha256="f898ce257e66cff9e29320458870570e55721d16cb000de7f2cc27de7fdef14f")
    version("6.3", sha256="e7f1d9ebfeb6ada37d42a286aaedb2e69335cbc857049dc5c5544bb51e7a8db8")
    version("6.2", sha256="2a81825a62a468bf5c56ef9d9677aa2eb88acf78d4f996cb49a7db98b94a6b16")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # These targets are defined in the Makefile. Some can be auto-detected by the
    # compiler name, others need to be explicitly set.
    make_target = [
        "xlf",
        "ftn",
        "titan-cray",
        "pgi",
        "pgi-nersc",
        "pgi-llnl",
        "ifort",
        "ifort-scorep",
        "ifort-gcc",
        "gfortran",
        "gfortran-clang",
        "g95",
        "pathscale-nersc",
        "cray-nersc",
        "gnu-nersc",
        "intel-nersc",
        "bluegene",
        "llvm",
    ]
    variant(
        "make_target",
        default="none",
        description="Predefined targets in the MPAS Makefile.",
        values=make_target.extend("none"),
        multi=False,
    )
    variant(
        "precision",
        default="double",
        description="MPAS will be built with double/single precision reals.",
        values=("double", "single"),
        multi=False,
    )

    depends_on("mpi")
    depends_on("parallelio")

    conflicts(
        "%oneapi@:2024.1",
        msg="ifx internal compiler error triggered by maps-model fixed in oneapi@2024.2",
    )

    patch("makefile.patch", when="@7.0")

    parallel = False

    resource(
        when="@6.2:6.3",
        name="MPAS-Data",
        git="https://github.com/MPAS-Dev/MPAS-Data.git",
        commit="33561790de8b43087ab850be833f51a4e605f1bb",
    )
    resource(
        when="@7.0:", name="MPAS-Data", git="https://github.com/MPAS-Dev/MPAS-Data.git", tag="v7.0"
    )

    def patch_makefile(self, action, targets):
        """Patch predefined flags in Makefile.
        MPAS Makefile uses strings rather Makefile variables for its compiler flags.
        This patch substitutes the strings with flags set in `target:`."""

        # Target `all:` does not contain any strings with compiler flags
        if action == "all":
            return

        sed = Executable("sed")
        for target in targets:
            key = target.split("=")[0]
            sed(
                "-i",
                "-e",
                "/^" + action + ":.*$/,/^$/s?" + key + '.*\\" \\\\?' + target + '\\" \\\\?1',
                "Makefile",
            )

    def target(self, model, action):
        spec = self.spec
        satisfies = spec.satisfies
        fflags = [self.compiler.openmp_flag]
        cppflags = ["-D_MPI"]
        if satisfies("%gcc"):
            fflags.extend(["-ffree-line-length-none", "-fconvert=big-endian", "-ffree-form"])
            if satisfies("precision=double"):
                fflags.extend(["-fdefault-real-8", "-fdefault-double-8"])
            cppflags.append("-DUNDERSCORE")
        elif satisfies("%fj"):
            fflags.extend(["-Free", "-Fwide", "-CcdRR8"])
        elif satisfies("%intel") or satisfies("%oneapi"):
            fflags.extend(["-convert big_endian", "-FR"])
            if satisfies("precision=double"):
                fflags.extend(["-r8"])

            cppflags.append("-DUNDERSCORE")
        targets = [
            "FC_PARALLEL={0}".format(spec["mpi"].mpifc),
            "CC_PARALLEL={0}".format(spec["mpi"].mpicc),
            "CXX_PARALLEL={0}".format(spec["mpi"].mpicxx),
            "FC_SERIAL={0}".format(spack_fc),
            "CC_SERIAL={0}".format(spack_cc),
            "CXX_SERIAL={0}".format(spack_cxx),
            "CFLAGS_OMP={0}".format(self.compiler.openmp_flag),
            "FFLAGS_OMP={0}".format(" ".join(fflags)),
            "CPPFLAGS={0}".format(" ".join(cppflags)),
            "PIO={0}".format(spec["parallelio"].prefix),
            "NETCDF={0}".format(spec["netcdf-c"].prefix),
            "NETCDFF={0}".format(spec["netcdf-fortran"].prefix),
        ]
        if satisfies("^parallelio+pnetcdf"):
            targets.append("PNETCDF={0}".format(spec["parallel-netcdf"].prefix))
        if self.spec.variants["precision"]:
            targets.extend(["PRECISION={0}".format(self.spec.variants["precision"].value)])

        if action == "all":
            # First try to guess by compiler name
            if os.path.basename(spack_fc) in self.make_target:
                action = os.path.basename(spack_fc)
            # Then overwrite with the optional variant if set
            if self.spec.variants["make_target"].value != "none":
                action = self.spec.variants["make_target"].value

        targets.extend(
            ["USE_PIO2=true", "CPP_FLAGS=-D_MPI", "OPENMP=true", "CORE={0}".format(model), action]
        )

        self.patch_makefile(action, targets)
        return targets

    def build(self, spec, prefix):
        copy_tree(
            join_path("MPAS-Data", "atmosphere"), join_path("src", "core_atmosphere", "physics")
        )
        make(*self.target("init_atmosphere", "all"), parallel=True)
        mkdir("bin")
        copy("init_atmosphere_model", "bin")
        copy("namelist.init_atmosphere", "bin")
        copy("streams.init_atmosphere", "bin")
        make(*self.target("init_atmosphere", "clean"))
        make(*self.target("atmosphere", "all"), parallel=True)
        copy("atmosphere_model", "bin")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
