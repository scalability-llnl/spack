# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libceed(MakefilePackage, CudaPackage, ROCmPackage):
    """The CEED API Library: Code for Efficient Extensible Discretizations."""

    homepage = "https://github.com/CEED/libCEED"
    git = "https://github.com/CEED/libCEED.git"

    maintainers("jedbrown", "v-dobrev", "tzanio", "jeremylt")

    license("BSD-2-Clause")

    version("develop", branch="main")
    version("0.12.0", tag="v0.12.0", commit="4018a20a98d451fac24765d3ddb936861647ce8d")
    version("0.11.0", tag="v0.11.0", commit="8ec64e9ae9d5df169dba8c8ee61d8ec8907b8f80")
    version("0.10.1", tag="v0.10.1", commit="74532b27052d94e943eb8bc76257fbd710103614")
    version("0.9", tag="v0.9.0", commit="d66340f5aae79e564186ab7514a1cd08b3a1b06b")
    version("0.8", tag="v0.8", commit="e8f234590eddcce2220edb1d6e979af7a3c35f82")
    version("0.7", tag="v0.7", commit="0bc92be5158efcbeb80d3d59240233bf5b2f748c")
    version(
        "0.6", commit="c7f533e01e2f3f6720fbf37aac2af2ffed225f60"
    )  # tag v0.6 + small portability fixes
    version("0.5", tag="v0.5", commit="12804ff7ea2ac608ae5494437379e4f626cf5cb7")
    version("0.4", tag="v0.4", commit="40b9dad77dea06a1608fa8b93a0d8b9c993ee43d")
    version("0.2", tag="v0.2", commit="113004cb41757b819325a4b3a8a7dfcea5156531")
    version("0.1", tag="v0.1", commit="74e0540e2478136394f75869675056eb6aba67cc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("occa", default=False, description="Enable OCCA backends")
    variant("debug", default=False, description="Enable debug build")
    variant("libxsmm", default=False, description="Enable LIBXSMM backend", when="@0.3:")
    variant("magma", default=False, description="Enable MAGMA backend", when="@0.6:")

    conflicts("+rocm", when="@:0.7")

    with when("+rocm"):
        depends_on("hip@3.8.0:", when="@0.8:")
        depends_on("hipblas@3.8.0:", when="@0.8:")

    conflicts("+occa", when="@0.9:")

    with when("+occa"):
        depends_on("occa@1.1.0", when="@0.7:")
        depends_on("occa@1.0.8:", when="@0.4")
        depends_on("occa@1.0.0-alpha.5,develop", when="@:0.2")
        depends_on("occa+cuda", when="+cuda")
        depends_on("occa~cuda", when="~cuda")

    depends_on("libxsmm", when="+libxsmm")

    depends_on("magma", when="+magma")

    patch("libceed-v0.8-hip.patch", when="@0.8+rocm")
    patch("pkgconfig-version-0.4.diff", when="@0.4")

    # occa: do not occaFree kernels
    # Repeated creation and freeing of kernels appears to expose a caching
    # bug in Occa.
    patch("occaFree-0.2.diff", when="@0.2")

    @property
    def common_make_opts(self):
        spec = self.spec
        compiler = self.compiler
        # Note: The occa package exports OCCA_DIR in the environment

        # Use verbose building output
        makeopts = ["V=1"]

        if spec.satisfies("@:0.2"):
            makeopts += ["NDEBUG=%s" % ("" if spec.satisfies("+debug") else "1")]

        elif spec.satisfies("@0.4:"):
            # Determine options based on the compiler:
            if spec.satisfies("+debug"):
                opt = "-g"
            elif compiler.name == "gcc":
                opt = "-O3 -g -ffp-contract=fast"
                if compiler.version >= ver(4.9):
                    opt += " -fopenmp-simd"
                if self.spec.target.family in ["x86_64", "aarch64"]:
                    opt += " -march=native"
            elif compiler.name == "apple-clang":
                opt = "-O3 -g -march=native -ffp-contract=fast"
                if compiler.version >= ver(10):
                    opt += " -fopenmp-simd"
            elif compiler.name == "clang":
                opt = "-O3 -g -march=native -ffp-contract=fast"
                if compiler.version >= ver(6):
                    opt += " -fopenmp-simd"
            elif compiler.name in ["xl", "xl_r"]:
                opt = "-O -g -qsimd=auto"
            elif compiler.name == "intel":
                opt = "-O3 -g"
                makeopts += ["CC_VENDOR=icc"]
            else:
                opt = "-O -g"
            # Note: spack will inject additional target-specific flags through
            # the compiler wrapper.
            makeopts += ["OPT=%s" % opt]

            if spec.satisfies("@0.7") and compiler.name in ["xl", "xl_r"]:
                makeopts += ["CXXFLAGS.XL=-qpic -std=c++11 -MMD"]

            if spec.satisfies("@:0.7") and "avx" in self.spec.target:
                makeopts.append("AVX=1")

            if spec.satisfies("+cuda"):
                makeopts += ["CUDA_DIR=%s" % spec["cuda"].prefix]
                makeopts += ["CUDA_ARCH=sm_%s" % spec.variants["cuda_arch"].value]
                if spec.satisfies("@:0.4"):
                    nvccflags = [
                        '-ccbin %s -Xcompiler "%s" -Xcompiler %s'
                        % (compiler.cxx, opt, compiler.cc_pic_flag)
                    ]
                    nvccflags = " ".join(nvccflags)
                    makeopts += ["NVCCFLAGS=%s" % nvccflags]
            else:
                # Disable CUDA auto-detection:
                makeopts += ["CUDA_DIR=/disable-cuda"]

            if spec.satisfies("+rocm"):
                makeopts += ["HIP_DIR=%s" % spec["hip"].prefix]
                amdgpu_target = ",".join(spec.variants["amdgpu_target"].value)
                makeopts += ["HIP_ARCH=%s" % amdgpu_target]
                if spec.satisfies("@0.8"):
                    makeopts += ["HIPBLAS_DIR=%s" % spec["hipblas"].prefix]

            if spec.satisfies("+libxsmm"):
                makeopts += ["XSMM_DIR=%s" % spec["libxsmm"].prefix]

            if spec.satisfies("+magma"):
                makeopts += ["MAGMA_DIR=%s" % spec["magma"].prefix]

        return makeopts

    def edit(self, spec, prefix):
        make("info", *self.common_make_opts)

    @property
    def build_targets(self):
        return self.common_make_opts

    @property
    def install_targets(self):
        return ["install", "prefix={0}".format(self.prefix)] + self.common_make_opts

    def check(self):
        make("prove", *self.common_make_opts, parallel=False)

    @when("@0.1")
    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install("ceed.h", prefix.include)
        mkdirp(prefix.lib)
        install("libceed.%s" % dso_suffix, prefix.lib)
        filter_file(r"^prefix=.*$", "prefix=%s" % prefix, "ceed.pc")
        filter_file(r"^includedir=\$\{prefix\}$", "includedir=${prefix}/include", "ceed.pc")
        filter_file(r"^libdir=\$\{prefix\}$", "libdir=${prefix}/lib", "ceed.pc")
        filter_file(r"Version:.*$", "Version: 0.1", "ceed.pc")
        mkdirp(prefix.lib.pkgconfig)
        install("ceed.pc", prefix.lib.pkgconfig)
