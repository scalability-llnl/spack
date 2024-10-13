# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Draco(CMakePackage):
    """Draco is an object-oriented component library geared towards numerically
    intensive, radiation (particle) transport applications built for parallel
    computing hardware. It consists of semi-independent packages and a robust
    build system."""

    homepage = "https://github.com/lanl/draco"
    url = "https://github.com/lanl/Draco/archive/draco-7_1_0.zip"
    git = "https://github.com/lanl/Draco.git"
    maintainers("KineticTheory")

    license("BSD-3-Clause-Open-MPI")

    version("develop", branch="develop")
    version("7.18.0", sha256="b210e202a06ffdaf149193b5cba164411fd508e20e573e1dfc46d1f56e3fffaa")
    version("7.14.1", sha256="b05c75f1b8ea1d4fac4900d897fb1c948b470826b174ed8b97b32c6da9f030bf")
    version("7.14.0", sha256="c8abf293d81c1b8020907557c20d8d2f2edf9ac7ae60a534eab052a8c3b7f99d")
    version("7.13.0", sha256="07a443df71d8d3720ced98f86821f714d2bfaa9f17a177c7f0465a59a1e9e719")
    version("7.12.0", sha256="a127c1c0af44b72775902e2386ed58ff0ebb1907d229e1300176142274c9abc2")
    version("7.11.0", sha256="a829984778fefd98c3c609ac10403df3eb06f02d57bdbc013634d0dc1ed5af29")
    version("7.10.0", sha256="3530263a23a648fc7ae65748568f0a725a8b2c9bac9a41cc3cb1250c4af579de")
    version("7.9.1", sha256="c8fd029d5b74afc68670f7d449d60c24f2d284c9d6a944a2d3dce6efeb6ad097")
    version("7.9.0", sha256="17b54301897da0d4f9b91fef15cc2ec5e6c65a8e8c1c09e6e7b516c0fb82b50f")
    version("7.8.0", sha256="f6de794457441f69025619be58810bca432f3e0dd773ea9b9a7977b1dc09530d")
    version("7.7.0", sha256="eb7fffbcba48e16524f619d261192ead129f968c59f3581f3217b89590812ddf")
    version("7.6.0", sha256="c2c6b329620d7bcb0f2fc14371f105dfb80a84e7c5adbb34620777034b15c7c9")
    version("7.5.0", sha256="0bb12b5f5ff60ba3087310c07da42e8d4f481ec4259daaa24ec240815a2e9dec")
    version("7.4.0", sha256="61da2c3feace0e92c5410c9e9e613708fdf8954b1367cdc62c415329b0ddab6e")
    version("7.3.0", sha256="dc47ef6c1e04769ea177a10fc6ddf506f3e1e8d36eb5d49f4bc38cc509e24f10")
    version("7.2.0", sha256="ac4eac03703d4b7344fa2390a54140533c5e1f6ea0d59ef1f1d525c434ebe639")
    version("7.1.0", sha256="eca6bb86eb930837fb5e09b76c85c200b2c1522267cc66f81f2ec11a8262b5c9")
    version("6.25.0", sha256="e27eba44f397e7d111ff9a45b518b186940f75facfc6f318d76bd0e72f987440")
    version("6.23.0", sha256="edf20308746c06647087cb4e6ae7656fd057a89091a22bcba8f17a52e28b7849")
    version("6.22.0", sha256="4d1ed54944450c4ec7d00d7ba371469506c6985922f48f780bae2580c9335b86")
    version("6.21.0", sha256="f1ac88041606cdb1dfddd3bc74db0f1e15d8fc9d0a1eed939c8aa0fa63a85b55")
    version("6.20.1", sha256="b1c51000c9557e0818014713fce70d681869c50ed9c4548dcfb2e9219c354ebe")
    version("6.20.0", sha256="a6e3142c1c90b09c4ff8057bfee974369b815122b01d1f7b57888dcb9b1128f6")

    variant("caliper", default=False, description="Enable caliper timers support")
    variant("cuda", default=False, description="Enable Cuda/GPU support")
    variant("eospac", default=True, description="Enable EOSPAC support")
    variant("fast_fma", default=False, description="Enable fast FMA operations")
    variant("lapack", default=True, description="Enable LAPACK wrapper")
    variant("libquo", default=True, description="Enable Quo wrapper")
    variant("parmetis", default=True, description="Enable Parmetis support")
    variant("pythontools", default=False, description="Enable support for extra python tools")
    variant("qt", default=False, description="Enable Qt support")
    variant("superlu_dist", default=True, description="Enable SuperLU-DIST support")

    depends_on("cmake@3.9:", when="@:6", type="build")
    depends_on("cmake@3.11:", when="@7.0.0:7.1", type="build")
    depends_on("cmake@3.14:", when="@7.2.0:7.6", type="build")
    depends_on("cmake@3.17:", when="@7.7:", type="build")
    depends_on("cmake@3.18:", when="@7.9:", type="build")
    depends_on("gsl@:2.5", when="@:7.10")
    depends_on("gsl@2.6:", when="@7.11.0:")
    depends_on("mpi@3:", type=("build", "link", "run"))
    depends_on("numdiff", type="build")
    depends_on("random123@1.09", when="@:7.6")
    depends_on("random123", when="@7.7.0:")
    depends_on("python@2.7:", when="@:7.6", type=("build", "run", "test"))
    depends_on("python@3.5:", when="@7.7.0:", type=("build", "run", "test"))

    # Optional dependencies
    depends_on("caliper", when="+caliper")
    depends_on("cuda@11.0:", when="+cuda")
    depends_on("eospac@6.3:", when="+eospac")
    depends_on("lapack", when="+lapack")
    depends_on("libquo@1.3.1:", when="@7.4.0:+libquo")
    depends_on("metis", when="+parmetis")
    depends_on("parmetis", when="+parmetis")
    depends_on("qt", when="+qt", type=("build", "link", "run"))
    depends_on("superlu-dist@:5", when="@:7.6+superlu_dist")
    depends_on("py-matplotlib", when="+pythontools", type=("run"))

    conflicts("+cuda", when="@:7.6")
    conflicts("+caliper", when="@:7.7")

    # Fix python discovery.
    patch("d710.patch", when="@7.1.0")
    patch("d730.patch", when="@7.3.0:7.3")
    patch("d740.patch", when="@7.4.0:7.4")
    patch("d750-intel17.patch", when="@7.5.0:7.6.99%intel@17.0.0:18.0.0")
    patch("d760-cray.patch", when="@7.6.0")
    patch("d770-nocuda.patch", when="@7.7.0")
    patch("d770-query_craype.patch", when="@7.7.0")
    patch("smpi.patch", when="@:7.6.99")
    patch("CMAKE-add-option-to-not-use-QT.patch", when="@7.8.0")

    def url_for_version(self, version):
        url = "https://github.com/lanl/Draco/archive/draco-{0}.zip"
        return url.format(version.underscored)

    def cmake_args(self):
        options = []
        options.extend(
            [
                "-Wno-dev",
                self.define("BUILD_TESTING", self.run_tests),
                "-DUSE_CUDA={0}".format("ON" if "+cuda" in self.spec else "OFF"),
                "-DUSE_QT={0}".format("ON" if "+qt" in self.spec else "OFF"),
            ]
        )
        if self.spec.satisfies("+fast_fma"):
            options.extend(
                [
                    "-DDRACO_ROUNDOFF_MODE={0}".format(
                        "FAST" if "build_type=Release" in self.spec else "ACCURATE"
                    )
                ]
            )
        return options

    def check(self):
        """Run ctest after building project."""
        with working_dir(self.build_directory):
            ctest("--output-on-failure")
