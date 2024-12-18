# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Enzo(MakefilePackage):
    """The Enzo adaptive mesh-refinement simulation code."""

    homepage = "https://enzo-project.org/"
    url = "https://github.com/enzo-project/enzo-dev/archive/enzo-2.6.1.tar.gz"
    git = "https://github.com/enzo-project/enzo-dev.git"

    version("main", branch="main")
    version("master", branch="main", deprecated=True)
    version("2.6.1", sha256="280270accfc1ddb60e92cc98ca538a3e5787e8cc93ed58fb5c3ab75db8c4b048")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("hdf5~mpi")
    depends_on("sse2neon", when="target=aarch64:")

    variant(
        "opt",
        default="high",
        description="Optimization, some compilers do not "
        + "produce stable code with high+ optimizations",
        values=("warn", "debug", "cudadebug", "high", "aggressive"),
        multi=False,
    )

    patch("for_aarch64.patch", when="target=aarch64:")

    # https://github.com/enzo-project/enzo-dev/pull/158
    patch(
        "https://github.com/enzo-project/enzo-dev/commit/0191ff5ad9ad2c7639d44823e84cd0115e7a2970.patch?full_index=1",
        sha256="f6db2fef04d3ffe4f05ef589d0593b2ab7ab6d63088abf9b76c7bacf835625c0",
        when="@2.6.1 ^hdf5@1.12.0:",
    )

    def flag_handler(self, name, flags):
        if name == "fflags":
            if self.spec.satisfies("%gcc@10:"):
                if flags is None:
                    flags = []
                flags.append("-fallow-argument-mismatch")

        return (flags, None, None)

    def edit(self, spec, prefix):
        configure = Executable("./configure")
        configure()

        with working_dir("src/enzo"):
            copy("Make.mach.linux-gnu", "Make.mach.spack")

            filter_file("^MACH_FILE.*", "MACH_FILE = Make.mach.spack", "Make.mach.spack")
            filter_file(
                "^LOCAL_HDF5_INSTALL.*",
                "LOCAL_HDF5_INSTALL = {0}".format(spec["hdf5"].prefix),
                "Make.mach.spack",
            )
            filter_file("^LOCAL_GRACKLE_INSTALL.*", "LOCAL_GRACKLE_INSTALL =", "Make.mach.spack")
            filter_file("^LOCAL_HYPRE_INSTALL.*", "LOCAL_HYPRE_INSTALL =", "Make.mach.spack")

    def build(self, spec, prefix):
        with working_dir("src/enzo"):
            make("machine-spack")
            make("opt-" + self.spec.variants["opt"].value)
            make("show-config")
            make()
        with working_dir("src/inits"):
            make()
        with working_dir("src/ring"):
            make()

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("doc", prefix.doc)
        install_tree("input", prefix.input)
        install_tree("run", prefix.run)
        install(join_path("src", "ring", "ring.exe"), join_path(prefix.bin, "ring"))
