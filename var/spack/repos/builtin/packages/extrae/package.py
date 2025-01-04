# Copyright Spack Project Developers. See COPYRIGHT file for details.
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
#   --with-elfutils=/usr
#   --with-tbb=/usr
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

    version("4.2.3", sha256="c132f3609b2e6f34d95ca1598eea01e5097257b6a663bb9698206ec271825ed0")
    version("4.2.2", sha256="1f776f1a3401942b79685ba13489a954a731bce7cbb8549594f6da0b557c58a7")
    version("4.2.1", sha256="0260a9a4952b6ac9b82ee33ee2749c22ae10d39447e42167a2626c77f664bb9a")
    version("4.2.0", sha256="7b83a1ed008440bbc1bda88297d2d0e9256780db1cf8401b3c12718451f8919a")
    version("4.1.7", sha256="0ed87449f74db0abc239ee8c40176e89f9ca6a69738fe751ec0df8fc46da1712")
    version("4.1.6", sha256="9f146e70311b8ae9d77584f6efc7b30478885cfd095f7bd3937d5b08aec19985")
    version("4.1.5", sha256="ab425f2e155e9af3332c01177df1776a6a953e721dfe8774eb23733f942b76a0")
    version("4.1.4", sha256="6b5894bea046273a0d2a5c72204937ad310b2f88cd5d87d10f5ca0aaf1d637da")
    version("4.1.3", sha256="889f136ddcfec2f8f9401b24ee29ebf74cf055e4e524c54821aba25513c24c03")
    version("4.1.2", sha256="adbc1d3aefde7649262426d471237dc96f070b93be850a6f15280ed86fd0b952")
    version("4.0.6", sha256="233be38035dd76f6877b1fd93d308e024e5d4ef5519d289f8e319cd6c58d0bc6")
    version("4.0.5", sha256="8f5eefa95f2e94a3b5f9b7f7cbaaed523862f190575ee797113b1e97deff1586")
    version("4.0.4", sha256="b867d395c344020c04e6630e9bfc10bf126e093df989d5563a2f3a6bc7568224")
    version("4.0.3", sha256="0d87509ec03584a629a879dccea10cf334f8243004077f6af3745aabb31e7250")
    version("3.8.3", sha256="a05e40891104e73e1019b193002dea39e5c3177204ea04495716511ddfd639cf")
    version("3.7.1", sha256="c83ddd18a380c9414d64ee5de263efc6f7bac5fe362d5b8374170c7f18360378")
    version("3.4.1", sha256="77bfec16d6b5eee061fbaa879949dcef4cad28395d6a546b1ae1b9246f142725")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

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
    depends_on("elf", type="link")
    depends_on("libxml2")
    depends_on("numactl")
    depends_on("binutils+libiberty@:2.33", when="@:4.0.1")
    depends_on("binutils+libiberty", when="@4.0.2:")
    depends_on("gettext")
    # gettext dependency added to find -lintl
    # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined

    build_directory = "spack-build"

    variant("dyninst", default=False, description="Use dyninst for dynamic code installation")
    with when("+dyninst"):
        depends_on("dyninst@10.1.0:")
        depends_on("elfutils", when="@4.1.2:")
        depends_on("intel-oneapi-tbb", when="@4.1.2:")

    variant("papi", default=True, description="Use PAPI to collect performance counters")
    depends_on("papi", when="+papi")

    variant("cuda", default=False, description="Enable support for tracing CUDA")
    depends_on("cuda", when="+cuda")

    variant("cupti", default=False, description="Enable CUPTI support")
    depends_on("cuda", when="+cupti")
    conflicts("+cupti", when="~cuda", msg="CUPTI requires CUDA")

    variant(
        "single-mpi-lib",
        default=False,
        description="Enable single MPI instrumentation library that supports both Fortran and C",
    )

    patch(
        "dyninst_instruction.patch",
        when="@:4.0.6 +dyninst",
        sha256="c1df1627b51b9d0f38711aee50ff11f30ffc34c43e520c39118157e9c31a927e",
    )

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
            if spec.satisfies("+papi")
            else ["--without-papi"]
        )

        if spec.satisfies("+dyninst"):
            args += ["--with-dyninst={spec['dyninst'].prefix}"]

            if spec.satisfies("@4.1.2:"):
                args += [
                    f"--with-elfutils={spec['elfutils'].prefix}",
                    f"--with-tbb={spec['tbb'].prefix}",
                ]
        else:
            args += ["--without-dyninst"]

        args += (
            ["--with-cuda=%s" % spec["cuda"].prefix]
            if spec.satisfies("+cuda")
            else ["--without-cuda"]
        )

        if spec.satisfies("+cupti"):
            cupti_h = find_headers("cupti", spec["cuda"].prefix, recursive=True)
            cupti_dir = os.path.dirname(os.path.dirname(cupti_h[0]))

        args += ["--with-cupti=%s" % cupti_dir] if "+cupti" in spec else ["--without-cupti"]

        if spec.satisfies("+dyninst"):
            make.add_default_arg("CXXFLAGS=%s" % self.compiler.cxx11_flag)
            args.append("CXXFLAGS=%s" % self.compiler.cxx11_flag)

        args.extend(self.enable_or_disable("single-mpi-lib"))

        # Library dir of -lintl as provided by gettext to be independent on the system's libintl
        args.append(f"LDFLAGS=-L{spec['gettext'].prefix.lib}")

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

        # This is to work around
        # <https://github.com/bsc-performance-tools/extrae/issues/115>.
        if self.spec.satisfies("%gcc@14:") and name == "cflags":
            flags.extend(
                [
                    "-Wno-error=incompatible-pointer-types",
                    "-Wno-error=implicit-function-declaration",
                    "-Wno-error=int-conversion",
                ]
            )

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
