# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nnpack(CMakePackage):
    """Acceleration package for neural networks on multi-core CPUs."""

    homepage = "https://github.com/Maratyszcza/NNPACK"
    git = "https://github.com/Maratyszcza/NNPACK.git"

    version("master", branch="master")
    version("2020-12-21", commit="c07e3a0400713d546e0dea2d5466dd22ea389c73")  # py-torch@1.8:1.9
    version("2019-10-07", commit="24b55303f5cf65d75844714513a0d1b1409809bd")  # py-torch@1.4:1.7
    version("2019-03-23", commit="c039579abe21f5756e0f0e45e8e767adccc11852")  # py-torch@1.1:1.3
    version("2018-09-03", commit="1e005b0c2777f39972a4ac15bea03e0e315a3d92")  # py-torch@1.0
    version("2018-05-21", commit="3eb0d453662d05a708f43b108bed9e17b705383e")  # py-torch@0.4.1
    version("2018-04-05", commit="b63fe1ba8963f1756b8decc593766615cee99c35")  # py-torch@:0.4.0

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    generator("ninja")
    depends_on("cmake@2.8.12:", type="build")
    depends_on("python", type="build")
    depends_on("py-setuptools", type="build")

    resource(
        name="six",
        url="https://files.pythonhosted.org/packages/source/s/six/six-1.11.0.tar.gz",
        sha256="70e8a77beed4562e7f14fe23a786b54f6296e34344c23bc42f07b15018ff98e9",
        destination="deps",
        placement="six",
    )
    resource(
        name="opcodes",
        url="https://files.pythonhosted.org/packages/source/o/opcodes/opcodes-0.3.13.tar.gz",
        sha256="1859c23143fe20daa4110be87a947cbf3eefa048da71dde642290213f251590c",
        destination="deps",
        placement="opcodes",
    )
    resource(
        name="peachpy",
        git="https://github.com/Maratyszcza/PeachPy.git",
        branch="master",
        destination="deps",
        placement="peachpy",
    )
    resource(
        name="cpuinfo",
        git="https://github.com/Maratyszcza/cpuinfo.git",
        branch="master",
        destination="deps",
        placement="cpuinfo",
    )
    resource(
        name="fp16",
        git="https://github.com/Maratyszcza/FP16.git",
        branch="master",
        destination="deps",
        placement="fp16",
    )
    resource(
        name="fxdiv",
        git="https://github.com/Maratyszcza/FXdiv.git",
        branch="master",
        destination="deps",
        placement="fxdiv",
    )
    resource(
        name="psimd",
        git="https://github.com/Maratyszcza/psimd.git",
        branch="master",
        destination="deps",
        placement="psimd",
    )
    resource(
        name="pthreadpool",
        git="https://github.com/Maratyszcza/pthreadpool.git",
        branch="master",
        destination="deps",
        placement="pthreadpool",
    )
    resource(
        name="googletest",
        url="https://github.com/google/googletest/archive/release-1.8.0.zip",
        sha256="f3ed3b58511efd272eb074a3a6d6fb79d7c2e6a0e374323d1e6bcbcc1ef141bf",
        destination="deps",
        placement="googletest",
    )

    @run_before("cmake")
    def generate_peachpy(self):
        # https://github.com/Maratyszcza/NNPACK/issues/203
        with working_dir(join_path(self.stage.source_path, "deps", "peachpy")):
            python("setup.py", "generate")

    def cmake_args(self):
        return [
            self.define("PYTHON_SIX_SOURCE_DIR", join_path(self.stage.source_path, "deps", "six")),
            self.define(
                "PYTHON_PEACHPY_SOURCE_DIR", join_path(self.stage.source_path, "deps", "peachpy")
            ),
            self.define(
                "CPUINFO_SOURCE_DIR", join_path(self.stage.source_path, "deps", "cpuinfo")
            ),
            self.define("FP16_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fp16")),
            self.define("FXDIV_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fxdiv")),
            self.define("PSIMD_SOURCE_DIR", join_path(self.stage.source_path, "deps", "psimd")),
            self.define(
                "PTHREADPOOL_SOURCE_DIR", join_path(self.stage.source_path, "deps", "pthreadpool")
            ),
            self.define(
                "GOOGLETEST_SOURCE_DIR", join_path(self.stage.source_path, "deps", "googletest")
            ),
            self.define("NNPACK_BUILD_TESTS", self.run_tests),
        ]
