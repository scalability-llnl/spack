# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.package import *


class Zoltan(AutotoolsPackage):
    """The Zoltan library is a toolkit of parallel combinatorial algorithms
    for parallel, unstructured, and/or adaptive scientific
    applications.  Zoltan's largest component is a suite of dynamic
    load-balancing and partitioning algorithms that increase
    applications' parallel performance by reducing idle time.  Zoltan
    also has graph coloring and graph ordering algorithms, which are
    useful in task schedulers and parallel preconditioners.

    """

    homepage = "https://sandialabs.github.io/Zoltan/"
    url = "https://github.com/sandialabs/Zoltan/archive/v3.83.tar.gz"

    license("Unlicense")

    version("3.901", sha256="030c22d9f7532d3076e40cba1f03a63b2ee961d8cc9a35149af4a3684922a910")
    version("3.83", sha256="17320a9f08e47f30f6f3846a74d15bfea6f3c1b937ca93c0ab759ca02c40e56c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("notparallel.patch", when="@3.8")

    variant("debug", default=False, description="Builds a debug version of the library.")
    variant("shared", default=True, description="Builds a shared version of the library.")

    variant("fortran", default=True, description="Enable Fortran support.")
    variant("mpi", default=True, description="Enable MPI support.")
    variant("parmetis", default=False, description="Enable ParMETIS support.")
    variant("int64", default=False, description="Enable 64bit indices.")

    depends_on("mpi", when="+mpi")

    depends_on("parmetis@4: +int64", when="+parmetis+int64")
    depends_on("parmetis@4:", when="+parmetis")
    depends_on("metis+int64", when="+parmetis+int64")
    depends_on("metis", when="+parmetis")

    depends_on("perl@:5.21", type="build", when="@:3.6")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("m4", type="build")

    conflicts("+parmetis", when="~mpi")

    build_directory = "spack-build"

    @property
    def configure_directory(self):
        spec = self.spec

        # FIXME: The older Zoltan versions fail to compile the F90 MPI wrappers
        # because of some complicated generic type problem.
        if spec.satisfies("@:3.6+fortran+mpi"):
            raise RuntimeError(
                (
                    "Cannot build Zoltan v{0} with +fortran and "
                    "+mpi; please disable one of these features "
                    "or upgrade versions."
                ).format(self.version)
            )
        if spec.satisfies("@:3.6"):
            zoltan_path = "Zoltan_v{0}".format(self.version)
            return zoltan_path
        return "."

    @property
    def parallel(self):
        # NOTE: Earlier versions of Zoltan cannot be built in parallel
        # because they contain nested Makefile dependency bugs.
        return not self.spec.satisfies("@:3.6+fortran")

    def autoreconf(self, spec, prefix):
        autoreconf = which("autoreconf")
        with working_dir(self.configure_directory):
            autoreconf("-ivf")

    def configure_args(self):
        spec = self.spec

        config_args = [
            self.get_config_flag("f90interface", "fortran"),
            self.get_config_flag("mpi", "mpi"),
        ]
        config_cflags = ["-O0" if "+debug" in spec else "-O3", "-g" if "+debug" in spec else ""]

        config_ldflags = []
        config_libs = []
        config_incdirs = []

        # PGI runtime libraries
        if "%pgi" in spec:
            config_ldflags.append("-pgf90libs")
        # NVHPC runtime libraries
        if "%nvhpc" in spec:
            config_ldflags.append("-fortranlibs")
        if "+shared" in spec:
            config_args.extend(["RANLIB=echo", "--with-ar=$(CXX) -shared $(LDFLAGS) -o"])
            config_cflags.append(self.compiler.cc_pic_flag)
            if spec.satisfies("%gcc"):
                config_libs.append("-lgfortran")
                # Although adding to config_libs _should_ suffice, it does not
                # Add to ldflags as well
                config_ldflags.append("-lgfortran")
            if spec.satisfies("%intel"):
                config_libs.append("-lifcore")

        if "+int64" in spec:
            config_args.append("--with-id-type=ulong")

        if "+parmetis" in spec:
            parmetis_prefix = spec["parmetis"].prefix
            config_args.extend(
                [
                    "--with-parmetis",
                    "--with-parmetis-libdir={0}".format(parmetis_prefix.lib),
                    "--with-parmetis-incdir={0}".format(parmetis_prefix.include),
                ]
            )
            config_ldflags.append("-L{0}".format(spec["metis"].prefix.lib))
            config_incdirs.append("-I{0}".format(spec["metis"].prefix.include))
            config_libs.append("-lparmetis")
            config_libs.append("-lmetis")
            # Although appending to config_libs _should_ suffice, it does not
            # Add them to ldflags as well
            config_ldflags.append("-lparmetis")
            config_ldflags.append("-lmetis")
            if "+int64" in spec["metis"]:
                config_args.append("--with-id-type=ulong")
            else:
                config_args.append("--with-id-type=uint")

        if "+mpi" in spec:
            config_args.extend(
                [
                    "CC={0}".format(spec["mpi"].mpicc),
                    "CXX={0}".format(spec["mpi"].mpicxx),
                    "--with-mpi={0}".format(spec["mpi"].prefix),
                    # NOTE: Zoltan assumes that it's linking against an MPI library
                    # that can be found with '-lmpi' which isn't the case for many
                    # MPI packages. We rely on the MPI-wrappers to automatically
                    # add what is required for linking and thus pass an empty
                    # list of libs
                    "--with-mpi-libs= ",
                ]
            )
            if "+fortran" in spec:
                config_args.extend(["FC={0}".format(spec["mpi"].mpifc)])

        config_fcflags = config_cflags[:]
        config_cxxflags = config_cflags[:]

        if spec.satisfies("%gcc@10:+fortran"):
            config_fcflags.append("-fallow-argument-mismatch")

        # NOTE: Early versions of Zoltan come packaged with a few embedded
        # library packages (e.g. ParMETIS, Scotch), which messes with Spack's
        # ability to descend directly into the package's source directory.
        if config_cflags:
            config_args.append("--with-cflags={0}".format(" ".join(config_cflags)))
        if config_cxxflags:
            config_args.append("--with-cxxflags={0}".format(" ".join(config_cxxflags)))
        if config_fcflags:
            config_args.append("--with-fcflags={0}".format(" ".join(config_fcflags)))
        if config_ldflags:
            config_args.append("--with-ldflags={0}".format(" ".join(config_ldflags)))
        if config_libs:
            config_args.append("--with-libs={0}".format(" ".join(config_libs)))
        if config_incdirs:
            config_args.append("--with-incdirs={0}".format(" ".join(config_incdirs)))
        return config_args

    # NOTE: Unfortunately, Zoltan doesn't provide any configuration
    # options for the extension of the output library files, so this
    # script must change these extensions as a post-processing step.
    @run_after("install")
    def solib_install(self):
        if "+shared" in self.spec:
            for lib_path in find(self.spec.prefix.lib, "lib*.a"):
                lib_shared_name = re.sub(r"\.a$", ".{0}".format(dso_suffix), lib_path)
                move(lib_path, lib_shared_name)

    def get_config_flag(self, flag_name, flag_variant):
        flag_pre = "en" if "+{0}".format(flag_variant) in self.spec else "dis"
        return "--{0}able-{1}".format(flag_pre, flag_name)
