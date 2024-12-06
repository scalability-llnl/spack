# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Aml(AutotoolsPackage):
    """AML is a memory management library designed to ease the use of complex
    memory topologies and complex data layout optimizations for
    high-performance computing applications.
    """

    homepage = "https://argo-aml.readthedocs.io/"

    maintainers("perarnau")

    test_requires_compiler = True

    tags = ["e4s"]

    # Package sources
    ###################################

    url = "https://github.com/anlsys/aml/releases/download/v0.2.0/aml-0.2.0.tar.gz"
    git = "https://github.com/anlsys/aml.git"

    license("ISC")

    # version string is generated from git tags, requires entire repo
    version("master", branch="master", submodules=True, get_full_repo=True)

    version("0.2.1", sha256="bae49e89ed0f2a2ad3547430e79b7e4c018d6228c6ed951a12d59afd0b35f71c")
    version("0.2.0", sha256="2044a2f3f1d7a19827dd9c0726172b690189b4d3fe938656c4160c022468cc4a")
    version(
        "0.1.0",
        sha256="cc89a8768693f1f11539378b21cdca9f0ce3fc5cb564f9b3e4154a051dcea69b",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    # Generate possible variants.
    #############################

    variant("opencl", default=False, description="Support for memory operations on top of OpenCL.")
    variant("ze", default=False, description="Support for memory operations on top of Level Zero.")
    variant("hip", default=False, description="Support for memory operations on top of HIP.")
    variant("cuda", default=False, description="Support for memory operations on top of CUDA.")
    variant("hwloc", default=True, description="Enable feature related to topology management")
    variant(
        "hip-platform",
        values=("none", conditional("amd", when="+hip"), conditional("nvidia", when="+cuda")),
        default="none",
        multi=False,
        description="HIP backend platform.",
    )

    # Dependencies management
    #########################

    # aml always depends on libnuma
    depends_on("numactl")

    # - cuda dependency. We use the environment variable CUDA_HOME in the configure.
    depends_on("cuda", when="+cuda")
    # - hip dependency. We use the environment variable HIP_PATH in the configure.
    depends_on("hip", when="+hip")
    # - level_zero loader is the dependency for the oneAPI variant
    depends_on("oneapi-level-zero", when="+ze")
    # - hwloc >= 2.1 becomes a dependency when +hwloc variant is used.
    depends_on("hwloc@2.1:", when="+hwloc")
    # - ocl-icd >= 2.1 becomes a dependency when +opencl variant is used.
    depends_on("ocl-icd@2.1:", when="+opencl")
    # Required on master for autoconf pull the right pkg.m4 macros,
    # and on other builds to detect dependencies
    # Note: This does NOT work with pkg-config but requires pkgconf!
    depends_on("pkgconf", type="build")

    # when on master, we need all the autotools and extras to generate files.
    with when("@master"):
        depends_on("m4", type="build")
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        # Required to generate AML version in configure.
        depends_on("git", type="build")

    # Configure options management
    ###########################################

    # This is the function to overload to pass all hwloc flag.
    def configure_args(self):
        config_args = []
        for b in ["opencl", "hwloc", "ze", "hip", "cuda"]:
            config_args.extend(self.with_or_without(b))
        if self.spec.satisfies("%oneapi"):
            config_args += ["--with-openmp-flags=-fiopenmp -fopenmp-targets=spir64"]
        if self.spec.variants["hip-platform"].value == "amd":
            config_args += ["--with-hip-platform=amd"]
        if self.spec.variants["hip-platform"].value == "nvidia":
            config_args += ["--with-hip-platform=nvidia"]
        return config_args

    # Tests
    #########################

    smoke_test = "0_hello"
    smoke_test_src = join_path("doc", "tutorials", "hello_world", smoke_test + ".c")

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, self.smoke_test_src)

    def test_check_tutorial(self):
        """Compile and run the tutorial tests as install checks"""
        cc = which(os.environ["CC"])
        cc_options = [
            "-o",
            self.smoke_test,
            join_path(self.test_suite.current_test_cache_dir, self.smoke_test_src),
            "-I{0}".format(self.prefix.include),
            "-I{0}".format(self.spec["numactl"].prefix.include),
            "-L{0}".format(self.prefix.lib),
            "-laml",
            "-lexcit",
            "-lpthread",
        ]
        cc(*cc_options)

        smoke_test = which(self.smoke_test)
        out = smoke_test(output=str.split, error=str.split)
        assert "Hello world" in out
