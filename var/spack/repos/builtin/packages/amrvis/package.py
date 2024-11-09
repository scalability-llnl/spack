# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Amrvis(MakefilePackage):
    """Amrvis is a visualization package specifically designed to
    read and display output and profiling data from codes built
    on the AMReX framework.
    """

    homepage = "https://github.com/AMReX-Codes/Amrvis"
    git = "https://github.com/AMReX-Codes/Amrvis.git"

    maintainers("etpalmer63")

    version("main", branch="main")

    depends_on("cxx", type="build")  # generated

    variant(
        "dims",
        default="3",
        values=("1", "2", "3"),
        multi=False,
        description="Number of spatial dimensions",
    )
    variant(
        "prec",
        default="DOUBLE",
        values=("FLOAT", "DOUBLE"),
        multi=False,
        description="Floating point precision",
    )
    variant("mpi", default=True, description="Enable MPI parallel support")
    variant("debug", default=False, description="Enable debugging features")
    variant("profiling", default=False, description="Enable AMReX profiling features")

    depends_on("gmake", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("libsm")
    depends_on("libice")
    depends_on("libxpm")
    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxext")
    depends_on("motif")
    depends_on("flex")
    depends_on("bison")

    conflicts("+profiling", when="dims=1", msg="Amrvis profiling support requires a 2D build")
    conflicts("+profiling", when="dims=3", msg="Amrvis profiling support requires a 2D build")

    # Only doing gcc and clang at the moment.
    # Intel currently fails searching for mpiicc, mpiicpc, etc.
    for comp in ["%intel", "%cce", "%nag", "%pgi", "%xl", "%xl_r"]:
        conflicts(comp, msg="Amrvis currently only builds with gcc and clang")

    # Need to clone AMReX into Amrvis because Amrvis uses AMReX's source
    resource(
        name="amrex",
        git="https://github.com/AMReX-Codes/amrex.git",
        tag="development",
        placement="amrex",
    )

    def edit(self, spec, prefix):
        # libquadmath is only available x86_64 and powerle
        # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=85440
        if self.spec.target.family not in ["x86_64", "ppc64le"]:
            comps = join_path("amrex", "Tools", "GNUMake", "comps")
            maks = [join_path(comps, "gnu.mak"), join_path(comps, "llvm.mak")]
            for mak in maks:
                filter_file("-lquadmath", "", mak)

        # Set all available makefile options to values we want
        makefile = FileFilter("GNUmakefile")
        makefile.filter(r"^AMREX_HOME\s*\?=.*", "AMREX_HOME = {0}".format("./amrex"))
        makefile.filter(r"^PRECISION\s*=.*", "PRECISION = {0}".format(spec.variants["prec"].value))
        makefile.filter(r"^DIM\s*=.*", "DIM = {0}".format(spec.variants["dims"].value))
        makefile.filter(
            r"^PROFILE\s*=.*", "PROFILE = {0}".format(spec.variants["profiling"].value).upper()
        )
        makefile.filter(
            r"^TRACE_PROFILE\s*=.*",
            "TRACE_PROFILE = {0}".format(spec.variants["profiling"].value).upper(),
        )
        makefile.filter(
            r"^COMM_PROFILE\s*=.*",
            "COMM_PROFILE = {0}".format(spec.variants["profiling"].value).upper(),
        )
        makefile.filter(r"^COMP\s*=.*", "COMP = {0}".format(self.compiler.name))
        makefile.filter(
            r"^DEBUG\s*=.*", "DEBUG = {0}".format(spec.variants["debug"].value).upper()
        )
        makefile.filter(r"^USE_ARRAYVIEW\s*=.*", "USE_ARRAY_VIEW = FALSE")
        makefile.filter(
            r"^USE_MPI\s*=.*", "USE_MPI = {0}".format(spec.variants["mpi"].value).upper()
        )
        makefile.filter(r"^USE_CXX11\s*=.*", "USE_CXX11 = TRUE")
        makefile.filter(r"^USE_VOLRENDER\s*=.*", "USE_VOLRENDER = FALSE")
        makefile.filter(r"^USE_PARALLELVOLRENDER\s*=.*", "USE_PARALLELVOLRENDER = FALSE")
        makefile.filter(
            r"^USE_PROFPARSER\s*=.*",
            "USE_PROFPARSER = {0}".format(spec.variants["profiling"].value).upper(),
        )

        # A bit risky here deleting all /usr and /opt X
        # library default search paths in makefile
        makefile.filter(
            r"^.*\b(usr|opt)\b.*$", "# Spack removed INCLUDE_LOCATIONS and LIBRARY_LOCATIONS"
        )

        # Rewrite configuration file with location of
        # the color palette after install
        configfile = FileFilter("amrvis.defaults")
        configfile.filter(r"^palette\s*Palette\s*", "palette {0}/etc/Palette\n".format(prefix))

        # Read GNUmakefile into array
        with open("GNUmakefile", "r") as file:
            contents = file.readlines()

        # Edit GNUmakefile includes and libraries to point to Spack
        # dependencies.
        # The safest bet is to put the LIBRARY_LOCATIONS and
        # INCLUDE_LOCATIONS at the beginning of the makefile.
        line_offset = 0
        count = 0
        for lib in ["libsm", "libice", "libxpm", "libx11", "libxt", "libxext", "motif"]:
            contents.insert(
                line_offset + count, "LIBRARY_LOCATIONS += {0}\n".format(spec[lib].prefix.lib)
            )
            contents.insert(
                line_offset + count + 1,
                "INCLUDE_LOCATIONS += {0}\n".format(spec[lib].prefix.include),
            )
            count += 1

        # Write GNUmakefile
        with open("GNUmakefile", "w") as file:
            file.writelines(contents)

    def setup_build_environment(self, env):
        # We don't want an AMREX_HOME the user may have set already
        env.unset("AMREX_HOME")
        # Help force Amrvis to not pick up random system compilers
        if self.spec.satisfies("+mpi"):
            env.set("MPI_HOME", self.spec["mpi"].prefix)
            env.set("CC", self.spec["mpi"].mpicc)
            env.set("CXX", self.spec["mpi"].mpicxx)
            env.set("F77", self.spec["mpi"].mpif77)
            env.set("FC", self.spec["mpi"].mpifc)
        # Set CONFIG_FILEPATH so Amrvis can find the configuration
        # file, amrvis.defaults.
        env.set("CONFIG_FILEPATH", self.spec.prefix.etc)

    def install(self, spec, prefix):
        # Install exe manually
        mkdirp(prefix.bin)
        install("*.ex", prefix.bin)
        # Install configuration file and default color Palette
        mkdirp(prefix.etc)
        install("amrvis.defaults", prefix.etc)
        install("Palette", prefix.etc)
