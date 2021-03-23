# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Genesis(AutotoolsPackage, CudaPackage):
    """GENESIS is a Molecular dynamics and modeling software
    for bimolecular systems such as proteins, lipids, glycans,
    and their complexes.
    """

    homepage = "https://www.r-ccs.riken.jp/labs/cbrt/"
    url = "https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2020/09/genesis-1.5.1.tar.bz2"
    git = "https://github.com/genesis-release-r-ccs/genesis-2.0.git"

    version("master", branch="master")
    version(
        "1.5.1",
        sha256="62a453a573c36779484b4ffed2dfa56ea03dfe1308d631b33ef03f733259b3ac",
        url="https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2020/09/genesis-1.5.1.tar.bz2",
    )

    resource(
        when="@1.5.1",
        name="user_guide",
        url="https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2019/10/GENESIS-1.4.0.pdf",
        sha256="da2c3f8bfa1e93adb992d3cfce09fb45d8d447a94f9a4f884ac834ea7279b9c7",
        expand=False,
        placement="doc",
    )

    variant("openmp", default=True, description="Enable OpenMP.")
    variant("single", default=False, description="Enable single precision.")
    variant("hmdisk", default=False, description="Enable huge molecule on hard disk.")

    conflicts("%apple-clang", when="+openmp")

    depends_on("autoconf", type="build", when="@1.5.1 %fj")
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@1.5.1 %fj")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@1.5.1 %fj")
    depends_on("libtool", type="build", when="@master")
    depends_on("m4", type="build", when="@1.5.1 %fj")
    depends_on("m4", type="build", when="@master")

    depends_on("mpi", type=("build", "run"))
    depends_on("lapack")
    depends_on("python@2.6.9:2.8.0", type=("build", "run"), when="@master")

    patch("fj_compiler.patch", when="@master %fj")
    patch("fj_compiler_1.5.1.patch", when="@1.5.1 %fj")

    parallel = False

    @property
    def force_autoreconf(self):
        # Run autoreconf due to build system patch
        return self.spec.satisfies("@1.5.1 %fj")

    def configure_args(self):
        spec = self.spec
        options = []
        options.extend(self.enable_or_disable("openmp"))
        options.extend(self.enable_or_disable("single"))
        options.extend(self.enable_or_disable("hmdisk"))
        if "+cuda" in spec:
            options.append("--enable-gpu")
            options.append("--with-cuda=%s" % spec["cuda"].prefix)
        else:
            options.append("--disable-gpu")
        if spec.target == "a64fx" and self.spec.satisfies("@master %fj"):
            options.append("--host=Fugaku")
        return options

    def setup_build_environment(self, env):
        env.set("FC", self.spec["mpi"].mpifc, force=True)
        env.set("F77", self.spec["mpi"].mpif77, force=True)
        env.set("CC", self.spec["mpi"].mpicc, force=True)
        env.set("CXX", self.spec["mpi"].mpicxx, force=True)
        env.set("LAPACK_LIBS", self.spec["lapack"].libs.ld_flags)
        if "+cuda" in self.spec:
            cuda_arch = self.spec.variants["cuda_arch"].value
            cuda_gencode = " ".join(self.cuda_flags(cuda_arch))
            env.set("NVCCFLAGS", cuda_gencode)

    def install(self, spec, prefix):
        make("install")
        install_tree("doc", prefix.share.doc)

    @run_after("install")
    def cache_test_sources(self):
        if self.spec.satisfies("@master"):
            self.cache_extra_test_sources(["tests"])

    def test(self):
        if self.spec.satisfies("@master"):
            exe_name = self.spec["python"].command.path
            test_name = join_path(
                self.install_test_root, "tests", "regression_test", "test.py"
            )
            bin_name = join_path(self.prefix.bin, "spdyn")
            opts = [
                test_name,
                self.spec["mpi"].prefix.bin.mpirun + " -np 8 " + bin_name,
            ]
            env["OMP_NUM_THREADS"] = "1"
            self.run_test(exe_name, options=opts, expected="Passed  53 / 53")
