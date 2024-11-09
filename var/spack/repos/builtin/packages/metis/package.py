# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *


class Metis(CMakePackage, MakefilePackage):
    """METIS is a set of serial programs for partitioning graphs, partitioning
    finite element meshes, and producing fill reducing orderings for sparse
    matrices.

    The algorithms implemented in METIS are based on the multilevel
    recursive-bisection, multilevel k-way, and multi-constraint partitioning schemes.
    """

    homepage = "http://glaros.dtc.umn.edu/gkhome/metis/metis/overview"
    url = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz"
    list_url = "http://glaros.dtc.umn.edu/gkhome/fsroot/sw/metis/OLD"

    # not a metis developer, just package reviewer!
    maintainers("mthcrts")

    license("Apache-2.0")

    version("5.1.0", sha256="76faebe03f6c963127dbb73c13eab58c9a3faeae48779f049066a21c087c5db2")
    version("4.0.3", sha256="5efa35de80703c1b2c4d0de080fafbcf4e0d363a21149a1ad2f96e0144841a55")

    depends_on("c", type="build")  # generated

    build_system(
        conditional("cmake", when="@5:"), conditional("makefile", when="@:4"), default="cmake"
    )
    variant("shared", default=True, description="Build shared libraries")
    with when("build_system=cmake"):
        variant("gdb", default=False, description="Enable gdb support")
        variant("int64", default=False, description="Use index type of 64 bit")
        variant("real64", default=False, description="Use real type of 64 bit")

        # Use the correct path to GKLIB when building out of source
        patch("gklib_path.patch")
        # Install both gklib_defs.h and gklib_rename.h
        patch("install_gklib_defs_rename.patch")
        # Disable the "misleading indentation" warning when compiling
        patch("gklib_nomisleadingindentation_warning.patch", when="%gcc@6:")

    with when("build_system=makefile"):
        variant("debug", default=False, description="Compile in debug mode")

    def patch(self):
        if not self.spec.satisfies("build_system=cmake"):
            return

        source_path = self.stage.source_path
        metis_header = FileFilter(join_path(source_path, "include", "metis.h"))

        metis_header.filter(
            r"(\b)(IDXTYPEWIDTH )(\d+)(\b)",
            r"\1\2{0}\4".format("64" if "+int64" in self.spec else "32"),
        )
        metis_header.filter(
            r"(\b)(REALTYPEWIDTH )(\d+)(\b)",
            r"\1\2{0}\4".format("64" if "+real64" in self.spec else "32"),
        )

        # Make clang 7.3 happy.
        # Prevents "ld: section __DATA/__thread_bss extends beyond end of file"
        # See upstream LLVM issue https://llvm.org/bugs/show_bug.cgi?id=27059
        # and https://github.com/Homebrew/homebrew-science/blob/master/metis.rb
        if self.spec.satisfies("%clang@7.3.0"):
            filter_file(
                "#define MAX_JBUFS 128",
                "#define MAX_JBUFS 24",
                join_path(source_path, "GKlib", "error.c"),
            )


class SetupEnvironment:
    def setup_build_environment(self, env):
        # Ignore warnings/errors re unrecognized omp pragmas on %intel
        if "%intel@14:" in self.spec:
            env.append_flags("CFLAGS", "-diag-disable 3180")
        # Ignore some warnings to get it to compile with %nvhpc
        #   111: statement is unreachable
        #   177: variable "foo" was declared but never referenced
        #   188: enumerated type mixed with another type
        #   550: variable "foo" was set but never used
        if "%nvhpc" in self.spec:
            env.append_flags("CFLAGS", "--display_error_number")
            env.append_flags("CFLAGS", "--diag_suppress 111")
            env.append_flags("CFLAGS", "--diag_suppress 177")
            env.append_flags("CFLAGS", "--diag_suppress 188")
            env.append_flags("CFLAGS", "--diag_suppress 550")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder, SetupEnvironment):
    @property
    def compile_options(self):
        options = []
        if "+shared" in self.spec:
            options.append(self.pkg.compiler.cc_pic_flag)
        if self.spec.satisfies("%cce@17:"):
            options.append("-std=c89")
        return options

    @property
    def optimize_options(self):
        options = []
        if "+debug" in self.spec:
            options.extend(["-g", "-O0"])
        else:
            options.append("-O2")  # default in Makefile.in
        return options

    @property
    def build_targets(self):
        options = []
        copts = self.compile_options
        oopts = self.optimize_options
        if copts:
            options.append("COPTIONS={0}".format(" ".join(copts)))
        if oopts:
            options.append("OPTFLAGS={0}".format(" ".join(oopts)))
        return options

    def install(self, pkg, spec, prefix):
        # Compile and install library files
        ccompile = Executable(pkg.compiler.cc)

        mkdir(prefix.bin)
        binfiles = (
            "pmetis",
            "kmetis",
            "oemetis",
            "onmetis",
            "partnmesh",
            "partdmesh",
            "mesh2nodal",
            "mesh2dual",
            "graphchk",
        )
        for binfile in binfiles:
            install(binfile, prefix.bin)

        mkdir(prefix.lib)
        install("libmetis.a", prefix.lib)

        mkdir(prefix.include)
        install(join_path("Lib", "*.h"), prefix.include)

        mkdir(prefix.share)
        sharefiles = (
            ("Graphs", "4elt.graph"),
            ("Graphs", "metis.mesh"),
            ("Graphs", "test.mgraph"),
        )
        for sharefile in tuple(join_path(*sf) for sf in sharefiles):
            install(sharefile, prefix.share)

        if "+shared" in spec:
            shared_flags = [pkg.compiler.cc_pic_flag, "-shared"]
            if sys.platform == "darwin":
                shared_suffix = "dylib"
                shared_flags.extend(["-Wl,-all_load", "libmetis.a"])
            else:
                shared_suffix = "so"
                shared_flags.extend(["-Wl,-whole-archive", "libmetis.a", "-Wl,-no-whole-archive"])

            shared_out = "%s/libmetis.%s" % (prefix.lib, shared_suffix)
            shared_flags.extend(["-o", shared_out])

            ccompile(*shared_flags)

        # Set up and run tests on installation
        ccompile(
            *self.compile_options,
            *self.optimize_options,
            "-I%s" % prefix.include,
            "-L%s" % prefix.lib,
            (pkg.compiler.cc_rpath_arg + prefix.lib if "+shared" in spec else ""),
            join_path("Programs", "io.o"),
            join_path("Test", "mtest.c"),
            "-o",
            "%s/mtest" % prefix.bin,
            "-lmetis",
            "-lm",
        )

    def check(self):
        test_bin = lambda testname: join_path(prefix.bin, testname)
        test_graph = lambda graphname: join_path(prefix.share, graphname)

        graph = test_graph("4elt.graph")
        os.system("%s %s" % (test_bin("mtest"), graph))
        os.system("%s %s 40" % (test_bin("kmetis"), graph))
        os.system("%s %s" % (test_bin("onmetis"), graph))
        graph = test_graph("test.mgraph")
        os.system("%s %s 2" % (test_bin("pmetis"), graph))
        os.system("%s %s 2" % (test_bin("kmetis"), graph))
        os.system("%s %s 5" % (test_bin("kmetis"), graph))
        graph = test_graph("metis.mesh")
        os.system("%s %s 10" % (test_bin("partnmesh"), graph))
        os.system("%s %s 10" % (test_bin("partdmesh"), graph))
        os.system("%s %s" % (test_bin("mesh2dual"), graph))


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder, SetupEnvironment):
    def cmake_args(self):
        options = [
            self.define_from_variant("SHARED", "shared"),
            self.define_from_variant("GDB", "gdb"),
        ]

        if self.spec.satisfies("~shared"):
            # Remove all RPATH options
            # (RPATHxxx options somehow trigger cmake to link dynamically)
            rpath_options = []
            for o in options:
                if o.find("RPATH") >= 0:
                    rpath_options.append(o)
            for o in rpath_options:
                options.remove(o)

        return options

    @run_after("install")
    def install_headers(self):
        with working_dir(self.build_directory):
            # install all headers, which will be needed for ParMETIS and other programs
            directories = ["GKlib", "libmetis", "programs"]
            for directory in directories:
                inc_dist = join_path(self.prefix.include, directory)
                mkdirp(inc_dist)
                install(join_path(self.stage.source_path, directory, "*.h"), inc_dist)

    def check(self):
        # On some systems, the installed binaries for METIS cannot
        # be executed without first being read.
        ls = which("ls")
        ls("-a", "-l", self.prefix.bin)

        graphchk = Executable(join_path(self.prefix.bin, "graphchk"))
        gpmetis = Executable(join_path(self.prefix.bin, "gpmetis"))
        ndmetis = Executable(join_path(self.prefix.bin, "ndmetis"))
        mpmetis = Executable(join_path(self.prefix.bin, "mpmetis"))
        for f in ["4elt", "copter2", "mdual"]:
            graph = join_path(self.stage.source_path, "graphs", "%s.graph" % f)
            graphchk(graph)
            gpmetis(graph, "2")
            ndmetis(graph)

        graph = join_path(self.stage.source_path, "graphs", "test.mgraph")
        gpmetis(graph, "2")
        graph = join_path(self.stage.source_path, "graphs", "metis.mesh")
        mpmetis(graph, "2")

    @run_after("install", when="+shared platform=darwin")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        fix_darwin_install_name(prefix.lib)
