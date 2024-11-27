# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Rose(AutotoolsPackage):
    """A compiler infrastructure to build source-to-source program
    transformation and analysis tools.
    (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    url = "https://github.com/rose-compiler/rose/archive/v0.9.13.0.zip"
    git = "https://github.com/rose-compiler/rose.git"

    maintainers("pinnown")

    # --------------------------------------------------------------------------
    # ROSE Versions
    # --------------------------------------------------------------------------

    license("BSD-3-Clause")

    version("0.9.13.0", sha256="64092793dfd38d476152696721e29a410bb31dc3eeb6064c7520087aa8c904a6")

    # Version for edg binary is found in src/frontend/CxxFrontend/EDG_VERSION
    # EDG_VERSION may be different from ROSE_VERSION
    resource(
        name="roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-4.9-5.0.9.12.52.tar.gz",
        expand=False,
        placement="rose-build/src/frontend/CxxFrontend/",
        when="@0.9.13.0 %gcc@4.9.0:4.9",
        url="http://edg-binaries.rosecompiler.org/roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-4.9-5.0.9.12.52.tar.gz",
        sha256="fb4b50606bdc681b864bbece46d344d7775780ffe7883aa96305d732c9c04a1c",
    )

    resource(
        name="roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-5-5.0.9.12.52.tar.gz",
        expand=False,
        placement="rose-build/src/frontend/CxxFrontend/",
        when="@0.9.13.0 %gcc@5.0:5",
        url="http://edg-binaries.rosecompiler.org/roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-5-5.0.9.12.52.tar.gz",
        sha256="584f8f721274f0f2d5c9a0c7701c045af99580ea7cd1d50999e20c2a897298fb",
    )

    resource(
        name="roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-6-5.0.9.12.52.tar.gz",
        expand=False,
        placement="rose-build/src/frontend/CxxFrontend/",
        when="@0.9.13.0 %gcc@6.0:6",
        url="http://edg-binaries.rosecompiler.org/roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-6-5.0.9.12.52.tar.gz",
        sha256="561cd5a944d0dd01689aa0bea8eccf30fc994cd20c4c05da7943c6f36cec25b5",
    )

    resource(
        name="roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-7-5.0.9.12.52.tar.gz",
        expand=False,
        placement="rose-build/src/frontend/CxxFrontend/",
        when="@0.9.13.0 %gcc@7.0:7",
        url="http://edg-binaries.rosecompiler.org/roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-7-5.0.9.12.52.tar.gz",
        sha256="800a178804e8b5e936942b4eb036cc61e5d5ad43551cb4fd901ec42ba7e7a176",
    )

    # git versions depends on internet connection at build time
    version("develop", branch="develop")

    # --------------------------------------------------------------------------
    # Dependencies
    # --------------------------------------------------------------------------
    depends_on("autoconf@2.69:", type="build")
    depends_on("automake@1.14:", type="build")
    depends_on("libtool@2.4:", type="build")
    depends_on("flex@2.6.4:", type="build")
    depends_on("bison@3.4.2:", type="build")

    # C++11 compatible boost and gcc versions required for +cxx11 variant:
    depends_on("boost@1.60.0:1.64.0,1.65.1,1.66.0:1.67.0 cxxstd=11", when="+cxx11")
    depends_on("boost@1.60.0:1.64.0,1.65.1,1.66.0:1.67.0", when="~cxx11")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    # --------------------------------------------------------------------------
    # Variants
    # --------------------------------------------------------------------------
    variant("debug", default=False, description="Enable compiler debugging symbols")
    variant("optimized", default=False, description="Enable compiler optimizations")

    variant("tests", default=False, description="Build the tests directory")
    variant("tutorial", default=False, description="Build the tutorial directory")

    variant("tools", default=False, description="Build a selection of ROSE based tools")

    variant("mvapich2_backend", default=False, description="Enable mvapich2 backend compiler")
    depends_on("mvapich2", when="+mvapich2_backend")

    variant("binanalysis", default=False, description="Enable binary analysis tooling")
    depends_on("libgcrypt", when="+binanalysis", type="build")
    depends_on("py-binwalk", when="+binanalysis", type="run")

    variant("c", default=True, description="Enable c language support")
    variant("cxx", default=True, description="Enable c++ language support")

    # Use spack install cxxflags=-std=c++11
    variant("cxx11", default=True, description="Enable c++11 language support")

    variant("fortran", default=False, description="Enable fortran language support")
    depends_on("java@8", when="+fortran")

    variant("z3", default=False, description="Enable z3 theorem prover")
    depends_on("z3", when="+z3")

    variant("edg_source", default=False, description="Use the EDG C/C++ frontend source code")
    depends_on("git", when="+edg_source")

    # ------------------------------------------------------------------------
    # ROSE-based Projects
    # ------------------------------------------------------------------------
    variant("codethorn", default=False, description="Enable the CodeThorn project")
    variant("autopar", default=False, description="Enable the autoParallelization project")
    variant("polyopt", default=False, description="Enable the PolyOpt project")

    build_directory = "rose-build"

    def autoreconf(self, spec, prefix):
        with working_dir(self.stage.source_path):
            bash = which("bash")
            bash("build")

        if "+edg_source" in spec:
            git = which("git")
            git(
                "clone",
                "rose-dev@rosecompiler1.llnl.gov:rose/edg4x/edg.git",
                "src/frontend/CxxFrontend/EDG",
            )

    @property
    def languages(self):
        spec = self.spec
        langs = [
            "binaries" if "+binanalysis" in spec else "",
            "c" if "+c" in spec else "",
            "c++" if "+cxx" in spec else "",
            "fortran" if "+fortran" in spec else "",
        ]
        return list(filter(None, langs))

    def configure_args(self):
        spec = self.spec

        if "+mvapich2_backend" in spec:
            cc = spec["mvapich2"].mpicc
            cxx = spec["mvapich2"].mpicxx
        else:
            cc = spack_cc
            cxx = spack_cxx

        args = [
            "--disable-boost-version-check",
            "--with-alternate_backend_C_compiler={0}".format(cc),
            "--with-alternate_backend_Cxx_compiler={0}".format(cxx),
            "--with-boost={0}".format(spec["boost"].prefix),
            "--enable-languages={0}".format(",".join(self.languages)),
        ]

        if "+z3" in spec:
            args.append("--with-z3={0}".format(spec["z3"].prefix))
        else:
            args.append("--without-z3")

        if "+tests" in spec:
            args.append("--enable-tests-directory")
        else:
            args.append("--disable-tests-directory")

        if "+tutorial" in spec:
            args.append("--enable-tutorial-directory")
        else:
            args.append("--disable-tutorial-directory")

        if "+fortran" in spec:
            args.append("--with-java={0}".format(spec["java"].prefix))
        else:
            args.append("--without-java")

        if "+debug" in spec:
            args.append("--with-CXX_DEBUG=-g")
        else:
            args.append("--without-CXX_DEBUG")

        if "+optimized" in spec:
            args.append("--with-C_OPTIMIZE=-O0")
            args.append("--with-CXX_OPTIMIZE=-O0")
        else:
            args.append("--without-C_OPTIMIZE")
            args.append("--without-CXX_OPTIMIZE")

        if "+cxx11" in spec:
            args.append("CXXFLAGS=-std=c++11")

        return args

    def setup_build_environment(self, env):
        if "+codethorn" in self.spec:
            env.set("CXXFLAGS", "-std=c++11")

    def build(self, spec, prefix):
        # Spack will automatically pass ncpus as the number of make jobs.
        #
        # If you really want to srun this on a separate node, you can do this:
        #
        #   $ srun -n1 spack install rose
        #
        with working_dir(self.build_directory):
            # Compile librose
            make("core")

            if "+tools" in spec:
                make("tools")

            # -----------------------------------------------------------------
            # ROSE-based Projects
            # -----------------------------------------------------------------
            if "+codethorn" in spec:
                with working_dir("projects/CodeThorn"):
                    make()

            if "+autopar" in spec:
                with working_dir("projects/autoParallelization"):
                    make()

            if "+polyopt" in spec:
                mkdir = which("mkdir")
                mkdir("-p", "projects/PolyOpt2")
                with working_dir("projects/PolyOpt2"):
                    env["ROSE_SRC"] = self.stage.source_path
                    env["ROSE_ROOT"] = self.prefix

                    bash = which("bash")
                    bash(join_path(self.stage.source_path, "projects/PolyOpt2/install.sh"))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            # Compile and Install librose
            make("install-core")

            if "+tools" in spec:
                make("install-tools")

            # -----------------------------------------------------------------
            # ROSE-based Projects
            # -----------------------------------------------------------------
            if "+codethorn" in spec:
                with working_dir("projects/CodeThorn"):
                    make("install")

            if "+autopar" in spec:
                with working_dir("projects/autoParallelization"):
                    make("install")
