# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class R(AutotoolsPackage):
    """R is 'GNU S', a freely available language and environment for
    statistical computing and graphics which provides a wide variety of
    statistical and graphical techniques: linear and nonlinear modelling,
    statistical tests, time series analysis, classification, clustering, etc.
    Please consult the R project homepage for further information."""

    homepage = "https://www.r-project.org"
    url = "https://cloud.r-project.org/src/base/R-4/R-4.4.0.tar.gz"

    extendable = True

    executables = ["^R$"]

    license("GPL-2.0-or-later")

    version("4.4.1", sha256="b4cb675deaaeb7299d3b265d218cde43f192951ce5b89b7bb1a5148a36b2d94d")
    version("4.4.0", sha256="ace4125f9b976d2c53bcc5fca30c75e30d4edc401584859cbadb080e72b5f030")
    version("4.3.3", sha256="80851231393b85bf3877ee9e39b282e750ed864c5ec60cbd68e6e139f0520330")
    version("4.3.2", sha256="b3f5760ac2eee8026a3f0eefcb25b47723d978038eee8e844762094c860c452a")
    version("4.3.1", sha256="8dd0bf24f1023c6f618c3b317383d291b4a494f40d73b983ac22ffea99e4ba99")
    version("4.3.0", sha256="45dcc48b6cf27d361020f77fde1a39209e997b81402b3663ca1c010056a6a609")
    version("4.2.3", sha256="55e4a9a6d43be314e2c03d0266a6fa5444afdce50b303bfc3b82b3979516e074")
    version("4.2.2", sha256="0ff62b42ec51afa5713caee7c4fde7a0c45940ba39bef8c5c9487fef0c953df5")
    version("4.2.1", sha256="4d52db486d27848e54613d4ee977ad952ec08ce17807e1b525b10cd4436c643f")
    version("4.2.0", sha256="38eab7719b7ad095388f06aa090c5a2b202791945de60d3e2bb0eab1f5097488")
    version("4.1.3", sha256="15ff5b333c61094060b2a52e9c1d8ec55cc42dd029e39ca22abdaa909526fed6")
    version("4.1.2", sha256="2036225e9f7207d4ce097e54972aecdaa8b40d7d9911cd26491fac5a0fab38af")
    version("4.1.1", sha256="515e03265752257d0b7036f380f82e42b46ed8473f54f25c7b67ed25bbbdd364")
    version("4.1.0", sha256="e8e68959d7282ca147360fc9644ada9bd161bab781bab14d33b8999a95182781")
    version("4.0.5", sha256="0a3ee079aa772e131fe5435311ab627fcbccb5a50cabc54292e6f62046f1ffef")
    version("4.0.4", sha256="523f27d69744a08c8f0bd5e1e6c3d89a4db29ed983388ba70963a3cd3a4a802e")
    version("4.0.3", sha256="09983a8a78d5fb6bc45d27b1c55f9ba5265f78fa54a55c13ae691f87c5bb9e0d")
    version("4.0.2", sha256="d3bceab364da0876625e4097808b42512395fdf41292f4915ab1fd257c1bbe75")
    version("4.0.1", sha256="95fe24a4d8d8f8f888460c8f5fe4311cec656e7a1722d233218bc03861bc6f32")
    version("4.0.0", sha256="06beb0291b569978484eb0dcb5d2339665ec745737bdfb4e873e7a5a75492940")
    version("3.6.3", sha256="89302990d8e8add536e12125ec591d6951022cf8475861b3690bc8bf1cefaa8f")
    version("3.6.2", sha256="bd65a45cddfb88f37370fbcee4ac8dd3f1aebeebe47c2f968fd9770ba2bbc954")
    version("3.6.1", sha256="5baa9ebd3e71acecdcc3da31d9042fb174d55a42829f8315f2457080978b1389")
    version("3.6.0", sha256="36fcac3e452666158e62459c6fc810adc247c7109ed71c5b6c3ad5fc2bf57509")
    version("3.5.3", sha256="2bfa37b7bd709f003d6b8a172ddfb6d03ddd2d672d6096439523039f7a8e678c")
    version("3.5.2", sha256="e53d8c3cf20f2b8d7a9c1631b6f6a22874506fb392034758b3bb341c586c5b62")
    version("3.5.1", sha256="0463bff5eea0f3d93fa071f79c18d0993878fd4f2e18ae6cf22c1639d11457ed")
    version("3.5.0", sha256="fd1725535e21797d3d9fea8963d99be0ba4c3aecadcf081b43e261458b416870")
    version("3.4.4", sha256="b3e97d2fab7256d1c655c4075934725ba1cd7cb9237240a11bb22ccdad960337")
    version("3.4.3", sha256="7a3cb831de5b4151e1f890113ed207527b7d4b16df9ec6b35e0964170007f426")
    version("3.4.2", sha256="971e30c2436cf645f58552905105d75788bd9733bddbcb7c4fbff4c1a6d80c64")
    version("3.4.1", sha256="02b1135d15ea969a3582caeb95594a05e830a6debcdb5b85ed2d5836a6a3fc78")
    version("3.4.0", sha256="288e9ed42457c47720780433b3d5c3c20983048b789291cc6a7baa11f9428b91")
    version("3.3.3", sha256="5ab768053a275084618fb669b4fbaadcc39158998a87e8465323829590bcfc6c")
    version("3.3.2", sha256="d294ad21e9f574fb4828ebb3a94b8cb34f4f304a41687a994be00dd41a4e514c")
    version("3.3.1", sha256="3dc59ae5831f5380f83c169bac2103ad052efe0ecec4ffa74bde4d85a0fda9e2")
    version("3.3.0", sha256="9256b154b1a5993d844bee7b1955cd49c99ad72cef03cce3cd1bdca1310311e4")
    version("3.2.5", sha256="60745672dce5ddc201806fa59f6d4e0ba6554d8ed78d0f9f0d79a629978f80b5")
    version("3.2.3", sha256="b93b7d878138279234160f007cb9b7f81b8a72c012a15566e9ec5395cfd9b6c1")
    version("3.2.2", sha256="9c9152e74134b68b0f3a1c7083764adc1cb56fd8336bec003fd0ca550cd2461d")
    version("3.2.1", sha256="d59dbc3f04f4604a5cf0fb210b8ea703ef2438b3ee65fd5ab536ec5234f4c982")
    version("3.2.0", sha256="f5ae953f18ba6f3d55b46556bbbf73441350f9fd22625402b723a2b81ff64f35")
    version("3.1.3", sha256="07e98323935baa38079204bfb9414a029704bb9c0ca5ab317020ae521a377312")
    version("3.1.2", sha256="bcd150afcae0e02f6efb5f35a6ab72432be82e849ec52ce0bb89d8c342a8fa7a")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("X", default=False, description="Enable X11 support (TCLTK, PNG, JPEG, TIFF, CAIRO)")
    variant("memory_profiling", default=False, description="Enable memory profiling")
    variant("rmath", default=False, description="Build standalone Rmath library")

    depends_on("blas")
    depends_on("lapack")

    depends_on("bzip2")
    depends_on("curl+libidn2")
    # R didn't anticipate the celebratory non-breaking major version bump of curl 8.
    depends_on("curl@:7", when="@:4.2")
    depends_on("icu4c")
    depends_on("java")
    depends_on("libtirpc")
    depends_on("ncurses")
    depends_on("pcre", when="@:3.6.3")
    depends_on("pcre2", when="@4:")
    depends_on("readline")
    depends_on("xz")
    depends_on("which", type=("build", "run"))
    depends_on("zlib-api")
    depends_on("zlib@1.2.5:", when="^[virtuals=zlib-api] zlib")
    depends_on("texinfo", type="build")

    with when("+X"):
        depends_on("cairo+X+gobject+pdf")
        depends_on("pango+X")
        depends_on("harfbuzz+graphite2")
        depends_on("jpeg")
        depends_on("libpng")
        depends_on("libtiff")
        depends_on("libx11")
        depends_on("libxmu")
        depends_on("libxt")
        depends_on("tk")

    patch("zlib.patch", when="@:3.3.2")

    # R cannot be built with '-O2' optimization
    # with Fujitsu Compiler @4.1.0 now.
    # Until the Fujitsu compiler resolves this problem,
    # temporary fix to lower the optimization level.
    patch("change_optflags_tmp.patch", when="%fj@4.1.0")

    # Make R use a symlink to which in Sys.which, otherwise an absolute path
    # gets stored as compressed byte code, which is not relocatable
    patch("relocate-which.patch")

    # CVE-2024-27322 Patch only needed in R 4.3.3 and below; doesn't apply to R older than 3.5.0.
    patch(
        "https://github.com/r-devel/r-svn/commit/f7c46500f455eb4edfc3656c3fa20af61b16abb7.patch?full_index=1",
        sha256="56c77763cb104aa9cb63420e585da63cb2c23bc03fa3ef9d088044eeff9d7380",
        when="@3.5.0:4.3.3",
    )

    build_directory = "spack-build"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        # R version 4.3.3 (2024-02-29) -- "Angel Food Cake"
        match = re.search(r"^R version ([^\s]+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        variants = []
        for exe in exes:
            output = Executable(exe)("CMD", "config", "--all", output=str, error=str)

            if "-lX11" in output:
                variants.append("+X")

        return variants

    # R custom URL version
    def url_for_version(self, version):
        """Handle R's customed URL versions"""
        url = "https://cloud.r-project.org/src/base"
        return url + "/R-%s/R-%s.tar.gz" % (version.up_to(1), version)

    @property
    def etcdir(self):
        return join_path(prefix, "rlib", "R", "etc")

    @run_after("install")
    def install_rmath(self):
        if "+rmath" in self.spec:
            with working_dir(join_path(self.build_directory, "src", "nmath", "standalone")):
                make()
                make("install", parallel=False)

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        extra_rpath = join_path(prefix, "rlib", "R", "lib")

        blas_flags: str = spec["blas"].libs.ld_flags
        lapack_flags: str = spec["lapack"].libs.ld_flags

        # R uses LAPACK in Fortran, which requires libmkl_gf_* when gfortran is used.
        # TODO: cleaning this up seem to require both compilers as dependencies and use variants.
        if spec["lapack"].name in INTEL_MATH_LIBRARIES and "gfortran" in self.compiler.fc:
            xlp64 = "ilp64" if spec["lapack"].satisfies("+ilp64") else "lp64"
            blas_flags = blas_flags.replace(f"mkl_intel_{xlp64}", f"mkl_gf_{xlp64}")
            lapack_flags = lapack_flags.replace(f"mkl_intel_{xlp64}", f"mkl_gf_{xlp64}")

        config_args = [
            "--with-internal-tzcode",
            "--libdir={0}".format(join_path(prefix, "rlib")),
            "--enable-R-shlib",
            "--enable-R-framework=no",
            "--without-recommended-packages",
            f"LDFLAGS=-Wl,-rpath,{extra_rpath}",
            f"--with-blas={blas_flags}",
            f"--with-lapack={lapack_flags}",
            # cannot disable docs with a normal configure option
            "ac_cv_path_PDFLATEX=",
            "ac_cv_path_PDFTEX=",
            "ac_cv_path_TEX=",
            "ac_cv_path_TEXI2DVI=",
        ]

        if "+X" in spec:
            config_args.append("--with-cairo")
            config_args.append("--with-jpeglib")
            config_args.append("--with-libpng")
            config_args.append("--with-libtiff")
            config_args.append("--with-tcltk")
            config_args.append("--with-x")

            tcl_config_path = join_path(spec["tcl"].libs.directories[0], "tclConfig.sh")
            config_args.append("--with-tcl-config={0}".format(tcl_config_path))

            tk_config_path = join_path(spec["tk"].libs.directories[0], "tkConfig.sh")
            config_args.append("--with-tk-config={0}".format(tk_config_path))
        else:
            config_args.append("--without-cairo")
            config_args.append("--without-jpeglib")
            config_args.append("--without-libpng")
            config_args.append("--without-libtiff")
            config_args.append("--without-tcltk")
            config_args.append("--without-x")

        if "+memory_profiling" in spec:
            config_args.append("--enable-memory-profiling")

        # Set FPICFLAGS for compilers except 'gcc'.
        if self.compiler.name != "gcc":
            config_args.append("FPICFLAGS={0}".format(self.compiler.cc_pic_flag))

        if self.spec.satisfies("@:3.6.1 %gcc@10:"):
            config_args.append("CFLAGS=-fcommon")
            config_args.append("FFLAGS=-fallow-argument-mismatch")

        return config_args

    @run_after("install")
    def copy_makeconf(self):
        # Make a copy of Makeconf because it will be needed to properly build R
        # dependencies in Spack.
        src_makeconf = join_path(self.etcdir, "Makeconf")
        dst_makeconf = join_path(self.etcdir, "Makeconf.spack")
        install(src_makeconf, dst_makeconf)

    # To respect order of execution, we should filter after we made the copy above
    filter_compiler_wrappers("Makeconf", relative_root=os.path.join("rlib", "R", "etc"))

    # ========================================================================
    # Set up environment to make install easy for R extensions.
    # ========================================================================

    @property
    def r_lib_dir(self):
        return join_path("rlib", "R", "library")

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Set R_LIBS to include the library dir for the
        # extension and any other R extensions it depends on.
        r_libs_path = []
        for d in dependent_spec.traverse(deptype=("build", "run")):
            if d.package.extends(self.spec):
                r_libs_path.append(join_path(d.prefix, self.r_lib_dir))

        r_libs_path = ":".join(r_libs_path)
        env.set("R_LIBS", r_libs_path)
        # R_LIBS_USER gets set to a directory in HOME/R if it is not set, such as
        # during package installation with the --vanilla flag. Set it to null
        # to ensure that it does not point to a directory that may contain R
        # packages.
        env.set("R_LIBS_USER", "")
        env.set("R_MAKEVARS_SITE", join_path(self.etcdir, "Makeconf.spack"))

        # Use the number of make_jobs set in spack. The make program will
        # determine how many jobs can actually be started.
        env.set("MAKEFLAGS", "-j{0}".format(make_jobs))
        env.set("R_HOME", join_path(self.prefix, "rlib", "R"))

    def setup_dependent_run_environment(self, env, dependent_spec):
        # For run time environment set only the path for dependent_spec and
        # prepend it to R_LIBS
        env.set("R_HOME", join_path(self.prefix, "rlib", "R"))
        if dependent_spec.package.extends(self.spec):
            env.prepend_path("R_LIBS", join_path(dependent_spec.prefix, self.r_lib_dir))

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "rlib", "R", "lib"))
        env.prepend_path("PKG_CONFIG_PATH", join_path(self.prefix, "rlib", "pkgconfig"))
        env.set("R_HOME", join_path(self.prefix, "rlib", "R"))

        if "+rmath" in self.spec:
            env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "rlib"))

    def setup_dependent_package(self, module, dependent_spec):
        """Called before R modules' install() methods. In most cases,
        extensions will only need to have one line:
            R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
              self.stage.source_path)"""

        # R extension builds can have a global R executable function
        module.R = Executable(join_path(self.spec.prefix.bin, "R"))

        # Add variable for library directry
        module.r_lib_dir = join_path(dependent_spec.prefix, self.r_lib_dir)
