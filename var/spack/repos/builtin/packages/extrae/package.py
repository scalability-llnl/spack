# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.boost import Boost

# typical working line with extrae 3.0.1
# ./configure
#   --prefix=/usr/local
#   --with-mpi=/usr/lib64/mpi/gcc/openmpi
#   --with-unwind=/usr/local
#   --with-papi=/usr
#   --with-dwarf=/usr
#   --with-elf=/usr
#   --with-dyninst=/usr
#   --with-binutils=/usr
#   --with-xml-prefix=/usr
#   --enable-openmp
#   --enable-nanos
#   --enable-pthread
#   --disable-parallel-merge
#
# LDFLAGS=-pthread


class Extrae(AutotoolsPackage):
    """Extrae is the package devoted to generate tracefiles which can
    be analyzed later by Paraver. Extrae is a tool that uses
    different interposition mechanisms to inject probes into the
    target application so as to gather information regarding the
    application performance. The Extrae instrumentation package can
    instrument the MPI programin model, and the following parallel
    programming models either alone or in conjunction with MPI :
    OpenMP, CUDA, OpenCL, pthread, OmpSs"""

    homepage = "https://tools.bsc.es/extrae"
    url = "https://ftp.tools.bsc.es/extrae/extrae-3.4.1-src.tar.bz2"

    license("LGPL-2.1-or-later")

    version("4.1.2", sha256="adbc1d3aefde7649262426d471237dc96f070b93be850a6f15280ed86fd0b952")
    version("4.0.6", sha256="b5060336cac57f1345faa09009b1940edf1e6991aae05cc10d0b714d31360a92")
    version("4.0.5", sha256="8f5eefa95f2e94a3b5f9b7f7cbaaed523862f190575ee797113b1e97deff1586")
    version("4.0.4", sha256="003bede870de6d88b705c1a13eabe63b6beb928d8f389f5dd70ca5db8450a1f9")
    version("4.0.3", sha256="b5139a07dbb1f4aa9758c1d62d54e42c01125bcfa9aa0cb9ee4f863afae93db1")
    version("3.8.3", sha256="c3bf27fb6f18e66200e40a0b4c35bc257766e5c1a525dc5725f561879e88bf32")
    version("3.7.1", sha256="c83ddd18a380c9414d64ee5de263efc6f7bac5fe362d5b8374170c7f18360378")
    version("3.4.1", sha256="77bfec16d6b5eee061fbaa879949dcef4cad28395d6a546b1ae1b9246f142725")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("mpi")
    depends_on("libunwind")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("libdwarf")
    depends_on("papi")
    depends_on("elf", type="link")
    depends_on("libxml2")
    depends_on("numactl")
    depends_on("binutils+libiberty@:2.33")
    depends_on("gettext")
    # gettext dependency added to find -lintl
    # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined

    build_directory = "spack-build"

    variant("dyninst", default=False, description="Use dyninst for dynamic code installation")
    depends_on("dyninst@:9", when="+dyninst")

    variant("papi", default=True, description="Use PAPI to collect performance counters")
    depends_on("papi", when="+papi")

    variant("cuda", default=False, description="Enable support for tracing CUDA")
    depends_on("cuda", when="+cuda")

    variant("cupti", default=False, description="Enable CUPTI support")
    depends_on("cuda", when="+cupti")
    conflicts("+cupti", when="~cuda", msg="CUPTI requires CUDA")

    def configure_args(self):
        spec = self.spec
        if spec.satisfies("^[virtuals=mpi] intel-oneapi-mpi"):
            mpiroot = spec["mpi"].component_prefix
        else:
            mpiroot = spec["mpi"].prefix

        args = [
            "--with-mpi=%s" % mpiroot,
            "--with-unwind=%s" % spec["libunwind"].prefix,
            "--with-boost=%s" % spec["boost"].prefix,
            "--with-dwarf=%s" % spec["libdwarf"].prefix,
            "--with-elf=%s" % spec["elf"].prefix,
            "--with-xml-prefix=%s" % spec["libxml2"].prefix,
            "--with-binutils=%s" % spec["binutils"].prefix,
        ]

        args += (
            ["--with-papi=%s" % spec["papi"].prefix]
            if "+papi" in self.spec
            else ["--without-papi"]
        )

        args += (
            ["--with-dyninst=%s" % spec["dyninst"].prefix]
            if "+dyninst" in self.spec
            else ["--without-dyninst"]
        )

        args += (
            ["--with-cuda=%s" % spec["cuda"].prefix]
            if "+cuda" in self.spec
            else ["--without-cuda"]
        )

        if self.spec.satisfies("+cupti"):
            cupti_h = find_headers("cupti", spec["cuda"].prefix, recursive=True)
            cupti_dir = os.path.dirname(os.path.dirname(cupti_h[0]))

        args += ["--with-cupti=%s" % cupti_dir] if "+cupti" in self.spec else ["--without-cupti"]

        if spec.satisfies("^dyninst@9.3.0:"):
            make.add_default_arg("CXXFLAGS=%s" % self.compiler.cxx11_flag)
            args.append("CXXFLAGS=%s" % self.compiler.cxx11_flag)

        return args

    def flag_handler(self, name, flags):
        # This was added due to:
        # - configure failure
        # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined
        # - linking error
        # https://github.com/bsc-performance-tools/extrae/issues/57
        if name == "ldlibs":
            if "intl" in self.spec["gettext"].libs.names:
                flags.append("-lintl")
        elif name == "ldflags":
            flags.append("-pthread")
        return self.build_system_flags(name, flags)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            # parallel installs are buggy prior to 3.7
            # see https://github.com/bsc-performance-tools/extrae/issues/18
            if spec.satisfies("@3.7:"):
                make("install", parallel=True)
            else:
                make("install", parallel=False)

    def setup_run_environment(self, env):
        # set EXTRAE_HOME in the module file
        env.set("EXTRAE_HOME", self.prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # set EXTRAE_HOME for everyone using the Extrae package
        env.set("EXTRAE_HOME", self.prefix)
