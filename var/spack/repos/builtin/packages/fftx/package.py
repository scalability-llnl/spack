# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Fftx(CMakePackage, CudaPackage, ROCmPackage):
    """FFTX is the exascale follow-on to the FFTW open source discrete FFT
    package for executing the Fast Fourier Transform as well as higher-level
    operations composed of linear operations combined with DFT transforms."""

    homepage = "https://spiralgen.com"
    url = "https://github.com/spiral-software/fftx/archive/refs/tags/1.2.0.tar.gz"
    git = "https://github.com/spiral-software/fftx.git"

    maintainers("spiralgen")

    license("BSD-3-Clause-LBNL")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.2.0", sha256="7be541bdb5905361e24bfb098314f946fe89f7b10f587d91e2397d821434b48b")
    version("1.1.3", sha256="17ed0baf9c2dcf30c789fdae530e006ae3ff2d2c9006989b1e6348e4ae50cef9")
    version("1.1.2", sha256="b2c4a7791305481af9e1bd358c1215efa4506c91c943cddca3780a1ccbc27810")
    version("1.1.1", sha256="5cbca66ef09eca02ee8f336f58eb45cfac69cfb29cd6eb945852ad74085d8a60")
    version("1.1.0", sha256="a6f95605abc11460bbf51839727a456a31488e27e12a970fc29a1b8c42f4e3b5")
    version("1.0.3", sha256="b5ff275facce4a2fbabd0aecc65dd55b744794f2e07cd8cfa91363001c664896")

    depends_on("cxx", type="build")  # generated

    depends_on("spiral-software+fftx+simt+jit+mpi")
    # depend only on spiral-software, but spiral-software must be installed with variants:
    # +fftx +simt +mpi +jit

    conflicts("+rocm", when="+cuda", msg="FFTX only supports one GPU backend at a time")

    @run_before("cmake")
    def create_lib_source_code(self):
        #  What config should be built -- driven by spec
        spec = self.spec
        backend = "CPU"
        if spec.satisfies("+cuda"):
            backend = "CUDA"
        if spec.satisfies("+rocm"):
            backend = "HIP"
        self.build_config = "-D_codegen=%s" % backend

        #  From the root directory run the config-fftx-libs.sh script
        with working_dir(self.stage.source_path):
            bash = which("bash")
            bash("./config-fftx-libs.sh", backend)

    def cmake_args(self):
        spec = self.spec
        args = ["-DSPIRAL_HOME:STRING={0}".format(spec["spiral-software"].prefix)]
        args.append("-DCMAKE_INSTALL_PREFIX:PATH={0}".format(self.prefix))
        if spec.satisfies("+rocm"):
            args.append("-DCMAKE_CXX_COMPILER={0}".format(self.spec["hip"].hipcc))
        args.append(self.build_config)

        print("Args = " + str(args))
        return args

    @property
    def build_targets(self):
        return ["install"]

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            files = ("License.txt", "README.md", "ReleaseNotes.md", "supercomputer-README.md")
            for fil in files:
                install(fil, prefix)

        mkdirp(prefix.cache_jit_files)
        with working_dir(self.stage.source_path):
            dir = join_path(self.stage.source_path, "cache_jit_files")
            if os.path.isdir(dir):
                install_tree("cache_jit_files", prefix.cache_jit_files)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("FFTX_HOME", self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("FFTX_HOME", self.prefix)

    def setup_run_environment(self, env):
        env.set("FFTX_HOME", self.prefix)
