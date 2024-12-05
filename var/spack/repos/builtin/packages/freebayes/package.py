# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freebayes(MesonPackage):
    """Bayesian haplotype-based genetic polymorphism discovery and
    genotyping."""

    homepage = "https://github.com/ekg/freebayes"
    url = "https://github.com/freebayes/freebayes/releases/download/v1.3.5/freebayes-1.3.5-src.tar.gz"
    git = "https://github.com/ekg/freebayes.git"

    license("MIT")

    version("1.3.6", sha256="6016c1e58fdf34a1f6f77b720dd8e12e13a127f7cbac9c747e47954561b437f5")
    version("1.3.5", sha256="7e2635690e916ed85cec36b3263e6e5357413a4f2bf3035362d9749335e8a696")
    version(
        "1.1.0",
        commit="39e5e4bcb801556141f2da36aba1df5c5c60701f",
        submodules=True,
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("zlib-api")

    # Deps for @1.3.5 and beyond
    depends_on("ninja", type="build", when="@1.3.5:")
    depends_on("pkgconfig", type="build", when="@1.3.5:")
    depends_on("htslib", when="@1.3.5:")
    depends_on("zlib-api", when="@1.3.5:")
    depends_on("xz", when="@1.3.5:")
    depends_on("parallel", when="@1.3.5:")
    depends_on("vcftools", when="@1.3.5:")
    depends_on("bc", when="@1.3.5:")
    depends_on("samtools", when="@1.3.5:")

    parallel = False

    @when("@:1.1.0")
    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        b = prefix.bin
        makefile.filter(
            "cp bin/freebayes bin/bamleftalign /usr/local/bin/",
            "cp bin/freebayes bin/bamleftalign {0}".format(b),
        )

    @when("@:1.1.0")
    @run_before("install")
    def make_prefix_dot_bin(self):
        mkdir(prefix.bin)

    @when("@:1.1.0")
    def meson(self, spec, prefix):
        pass

    @when("@:1.1.0")
    def build(self, spec, prefix):
        make()

    @when("@:1.1.0")
    def install(self, spec, prefix):
        make("install")

    @property
    def vcflib_builddir(self):
        return join_path(self.build_directory, "vcflib")

    @when("@1.3.4:")
    def setup_build_environment(self, env):
        if self.run_tests:
            env.prepend_path("PATH", self.vcflib_builddir)
            env.prepend_path("PATH", self.build_directory)

    @when("@1.3.4:")
    def check(self):
        mkdir(self.vcflib_builddir)
        with working_dir(self.vcflib_builddir):
            cmake("../../vcflib")
            make()
        with working_dir(self.build_directory):
            ninja("test")
