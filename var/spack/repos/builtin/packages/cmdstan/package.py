# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cmdstan(MakefilePackage):
    """CmdStan is the command line interface to Stan."""

    homepage = "https://mc-stan.org/users/interfaces/cmdstan"
    url = "https://github.com/stan-dev/cmdstan/releases/download/v2.30.1/cmdstan-2.30.1.tar.gz"

    license("BSD-3-Clause")

    version("2.30.1", sha256="bab76dcefa7f4c955595c0bf0496770507fc6ab0df5896e8cf8c2db0a17eedb9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("threads", default=True, description="enable thread support")
    variant("opencl", default=False, description="enable OpenCl support")
    variant("mpi", default=False, description="enable MPI support")

    depends_on("opencl", when="+opencl")
    depends_on("mpi", when="+mpi")

    build_targets = ["build"]

    filter_compiler_wrappers("local", relative_root="make")

    def edit(self, spec, prefix):
        if spec.satisfies("%intel"):
            cxx_type = "icc"
        else:
            cxx_type = spec.compiler.name

        if spec.satisfies("+mpi"):
            cxx = spec["mpi"].mpicxx
        else:
            cxx = spack_cxx

        make_options = [
            "CXX={0}\n".format(cxx),
            "CXXFLAGS+= -O2 -funroll-loops\n",
            "LDFLAGS+={0}{1}\n".format(
                self.compiler.cc_rpath_arg,
                join_path(prefix, "stan", "lib", "stan_math", "lib", "tbb"),
            ),
            "STANCFLAGS+= --warn-pedantic\n",
            "TBB_CXX_TYPE={0}\n".format(cxx_type),
        ]

        if spec.satisfies("+threads"):
            make_options.append("STAN_THREADS=true\n")

        if spec.satisfies("+opencl"):
            make_options.append("STAN_OPENCL=true\n")

        if spec.satisfies("+mpi"):
            make_options.append("STAN_MPI=true\n")

        filepath = join_path(self.stage.source_path, "make", "local")
        with open(filepath, "w") as make_file:
            make_file.writelines(make_options)

    def install(self, spec, prefix):
        make(join_path("examples", "bernoulli", "bernoulli"))

        mkdir(prefix.bin)

        with working_dir(self.build_directory):
            copy("makefile", prefix)
            copy_tree("make", prefix.make)
            copy_tree("examples", prefix.examples)
            copy_tree("lib", prefix.lib)
            copy_tree("src", prefix.src)
            copy_tree("stan", prefix.stan)

        with working_dir(join_path(self.build_directory, "bin")):
            install("diagnose", prefix.bin)
            install("print", prefix.bin)
            install("stanc", prefix.bin)
            install("stansummary", prefix.bin)

    def setup_run_environment(self, env):
        env.set("CMDSTAN", self.prefix)
