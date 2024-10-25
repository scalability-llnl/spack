# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path

import llnl.util.lang

from spack.package import *


class FftwBase(AutotoolsPackage):
    """Base class for building Fftw, shared with the AMD optimized version
    of the library in the 'amdfftw' package.
    """

    variant(
        "precision",
        values=any_combination_of("float", "double", "long_double", "quad")
        .prohibit_empty_set()
        .with_default("float,double"),
        description="Build the selected floating-point precision libraries",
    )
    variant("openmp", default=False, description="Enable OpenMP support.")
    variant("mpi", default=True, description="Activate MPI support")
    variant("shared", default=True, description="Build shared libraries")

    depends_on("mpi", when="+mpi")
    depends_on("llvm-openmp", when="%apple-clang +openmp")

    # https://github.com/FFTW/fftw3/commit/902d0982522cdf6f0acd60f01f59203824e8e6f3
    conflicts("%gcc@8.0:8", when="@3.3.7")
    conflicts(
        "precision=long_double",
        when="@2.1.5",
        msg="Long double precision is not supported in FFTW 2",
    )
    conflicts("precision=quad", when="@2.1.5", msg="Quad precision is not supported in FFTW 2")
    conflicts("precision=quad", when="+mpi", msg="Quad precision is not supported in MPI")

    @property
    def libs(self):
        # Reduce repetitions of entries
        query_parameters = list(llnl.util.lang.dedupe(self.spec.last_query.extra_parameters))

        # List of all the suffixes associated with float precisions
        precisions = [("float", "f"), ("double", ""), ("long_double", "l"), ("quad", "q")]

        # Retrieve the correct suffixes, or use double as a default
        suffixes = [v for k, v in precisions if k in query_parameters] or [""]

        # Construct the list of libraries that needs to be found
        libraries = []
        for sfx in suffixes:
            if "mpi" in query_parameters and "+mpi" in self.spec:
                libraries.append("libfftw3" + sfx + "_mpi")

            if "openmp" in query_parameters and "+openmp" in self.spec:
                libraries.append("libfftw3" + sfx + "_omp")

            libraries.append("libfftw3" + sfx)

        return find_libraries(libraries, root=self.prefix, recursive=True)

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%clang@15:"):
                flags.append("-Wno-error=int-conversion")

        return flags, None, None

    def patch(self):
        # If fftw/config.h exists in the source tree, it will take precedence
        # over the copy in build dir.  As only the latter has proper config
        # for our build, this is a problem.  See e.g. issue #7372 on github
        if os.path.isfile("fftw/config.h"):
            os.rename("fftw/config.h", "fftw/config.h.SPACK_RENAMED")

    def autoreconf(self, spec, prefix):
        if spec.satisfies("+pfft_patches"):
            autoreconf = which("autoreconf")
            autoreconf("-ifv")

    @property
    def selected_precisions(self):
        """Precisions that have been selected in this build"""
        return self.spec.variants["precision"].value

    def setup_build_environment(self, env):
        if self.spec.satisfies("%apple-clang +openmp"):
            env.append_flags("CPPFLAGS", self.compiler.openmp_flag)
            env.append_flags("CFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("CXXFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["llvm-openmp"].libs.ld_flags)
        # FFTW first configures libtool without MPI, and later uses it with
        # MPI. libtool then calls wrong linker to create shared libraries
        # (it calls `$CC` instead of `$MPICC`), and MPI symbols
        # remain undefined because `-lmpi` is not passed to the linker.
        # https://github.com/FFTW/fftw3/issues/274
        # https://github.com/spack/spack/issues/29224
        if self.spec.satisfies("+mpi") and self.spec.satisfies("platform=darwin"):
            env.append_flags("LIBS", self.spec["mpi"].libs.ld_flags)

    def configure(self, spec, prefix):
        # Base options
        options = ["--prefix={0}".format(prefix), "--enable-threads"]
        options.extend(self.enable_or_disable("shared"))

        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")
        if spec.satisfies("@:2"):
            options.append("--enable-type-prefix")

        # Variants that affect every precision
        if spec.satisfies("+openmp"):
            options.append("--enable-openmp")
            if spec.satisfies("@:2"):
                # TODO: libtool strips CFLAGS, so 2.x libxfftw_threads
                #       isn't linked to the openmp library. Patch Makefile?
                options.insert(0, "CFLAGS=" + self.compiler.openmp_flag)
        if spec.satisfies("+mpi"):
            options.append("--enable-mpi")

        # Specific SIMD support.
        # all precisions
        simd_features = ["sse2", "avx", "avx2", "avx512", "avx-128-fma", "kcvi", "vsx"]
        # float only
        float_simd_features = ["altivec", "sse", "neon"]

        # Workaround PGI compiler bug when avx2 is enabled
        if spec.satisfies("%pgi") and "avx2" in simd_features:
            simd_features.remove("avx2")

        # Workaround NVIDIA/PGI compiler bug when avx512 is enabled
        if spec.satisfies("%nvhpc") or spec.satisfies("%pgi"):
            if "avx512" in simd_features:
                simd_features.remove("avx512")

        # NVIDIA compiler does not support Altivec intrinsics
        if spec.satisfies("%nvhpc") and "vsx" in simd_features:
            simd_features.remove("vsx")
        if spec.satisfies("%nvhpc") and "altivec" in float_simd_features:
            float_simd_features.remove("altivec")

        # NVIDIA compiler does not support Neon intrinsics
        if spec.satisfies("%nvhpc") and "neon" in simd_features:
            simd_features.remove("neon")

        simd_options = []
        for feature in simd_features:
            msg = "--enable-{0}" if feature in spec.target else "--disable-{0}"
            simd_options.append(msg.format(feature))

        # If no features are found, enable the generic ones
        if not any(f in spec.target for f in simd_features + float_simd_features):
            # Workaround NVIDIA compiler bug
            if not spec.satisfies("%nvhpc"):
                simd_options += ["--enable-generic-simd128", "--enable-generic-simd256"]

        simd_options += ["--enable-fma" if "fma" in spec.target else "--disable-fma"]

        # Double is the default precision, for all the others we need
        # to enable the corresponding option.
        enable_precision = {
            "float": ["--enable-float"],
            "double": None,
            "long_double": ["--enable-long-double"],
            "quad": ["--enable-quad-precision"],
        }

        # Different precisions must be configured and compiled one at a time
        configure = Executable("../configure")
        for precision in self.selected_precisions:
            opts = (enable_precision[precision] or []) + options[:]

            # SIMD optimizations are available only for float and double
            # starting from FFTW 3
            if precision in ("float", "double") and spec.satisfies("@3:"):
                opts += simd_options

            # float-only acceleration
            if precision == "float":
                for feature in float_simd_features:
                    if feature in spec.target:
                        msg = "--enable-{0}"
                    else:
                        msg = "--disable-{0}"
                    opts.append(msg.format(feature))

            with working_dir(precision, create=True):
                configure(*opts)

    def for_each_precision_make(self, *targets):
        for precision in self.selected_precisions:
            with working_dir(precision):
                make(*targets)

    def build(self, spec, prefix):
        self.for_each_precision_make()

    def check(self):
        self.for_each_precision_make("check")

    def install(self, spec, prefix):
        self.for_each_precision_make("install")


class Fftw(FftwBase):
    """FFTW is a C subroutine library for computing the discrete Fourier
    transform (DFT) in one or more dimensions, of arbitrary input
    size, and of both real and complex data (as well as of even/odd
    data, i.e. the discrete cosine/sine transforms or DCT/DST). We
    believe that FFTW, which is free software, should become the FFT
    library of choice for most applications."""

    homepage = "https://www.fftw.org"
    url = "https://www.fftw.org/fftw-3.3.4.tar.gz"
    list_url = "https://www.fftw.org/download.html"

    license("GPL-2.0-or-later")

    version("3.3.10", sha256="56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467")
    version("3.3.9", sha256="bf2c7ce40b04ae811af714deb512510cc2c17b9ab9d6ddcf49fe4487eea7af3d")
    version("3.3.8", sha256="6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303")
    version("3.3.7", sha256="3b609b7feba5230e8f6dd8d245ddbefac324c5a6ae4186947670d9ac2cd25573")
    version("3.3.6-pl2", sha256="a5de35c5c824a78a058ca54278c706cdf3d4abba1c56b63531c2cb05f5d57da2")
    version("3.3.5", sha256="8ecfe1b04732ec3f5b7d279fdb8efcad536d555f9d1e8fabd027037d45ea8bcf")
    version("3.3.4", sha256="8f0cde90929bc05587c3368d2f15cd0530a60b8a9912a8e2979a72dbe5af0982")
    version("2.1.5", sha256="f8057fae1c7df8b99116783ef3e94a6a44518d49c72e2e630c24b689c6022630")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "pfft_patches",
        default=False,
        description="Add extra transpose functions for PFFT compatibility",
    )

    depends_on("automake", type="build", when="+pfft_patches")
    depends_on("autoconf", type="build", when="+pfft_patches")
    depends_on("libtool", type="build", when="+pfft_patches")

    provides("fftw-api@2", when="@2.1.5")
    provides("fftw-api@3", when="@3:")

    patch("pfft-3.3.9.patch", when="@3.3.9:+pfft_patches", level=0)
    patch(
        "https://github.com/FFTW/fftw3/commit/f69fef7aa546d4477a2a3fd7f13fa8b2f6c54af7.patch?full_index=1",
        sha256="872cff9a7d346e91a108ffd3540bfcebeb8cf86c7f40f6b31fd07a80267cbf53",
        when="@3.3.7:",
    )
    patch("pfft-3.3.5.patch", when="@3.3.5:3.3.8+pfft_patches", level=0)
    patch("pfft-3.3.4.patch", when="@3.3.4+pfft_patches", level=0)
    patch("pgi-3.3.6-pl2.patch", when="@3.3.6-pl2%pgi", level=0)
    patch("intel-configure.patch", when="@3:3.3.8%intel", level=0)
