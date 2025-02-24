# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.filesystem as fs

from spack import build_systems
from spack.package import *


class PyTriton(PythonPackage):
    """A language and compiler for custom Deep Learning operations."""

    homepage = "https://github.com/triton-lang/triton"
    url = "https://github.com/triton-lang/triton/archive/refs/tags/v2.1.0.tar.gz"
    git = "https://github.com/triton-lang/triton.git"

    license("MIT")

    version("main", branch="main")
    # new versions are no longer tagged and pypi does not provide source distributions
    version("3.2.0", commit="c802bb4fbe492b2d34405313a4f4d96d8f91a4d8")
    version("3.1.0", commit="5fe38ffd73c2ac6ed6323b554205186696631c6f")
    version("2.1.0", sha256="4338ca0e80a059aec2671f02bfc9320119b051f378449cf5f56a1273597a3d99")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    with default_args(type="build"):
        depends_on("py-setuptools@40.8:")
        depends_on("cmake@3.18:")
        depends_on("ninja")

    with default_args(type=("build", "link", "run")):
        depends_on("py-pybind11")
        depends_on("cuda")

    depends_on("py-filelock", type=("build", "run"))
    depends_on("zlib-api", type="link")

    conflicts("^openssl@3.3.0")

    # avoid bdist_whell.dist_info_dir problems:
    # pypa used to contain `bdist_wheel` but it is part of setuptools as of v70.1
    # these patches change
    #     wheel.bdist_wheel -> setuptools.command.bdist_wheel.bdist_wheel
    # see https://github.com/pypa/wheel/pull/631
    # and https://github.com/pypa/setuptools/pull/4684
    patch("setup_v3.1.0.patch", when="@3.1.0 ^py-setuptools@70.1:")
    patch("setup_v3.2.0.patch", when="@3.2.0 ^py-setuptools@70.1:")

    def setup_build_environment(self, env):
        """Set environment variables used to control the build"""
        if self.spec.satisfies("%clang"):
            env.set("TRITON_BUILD_WITH_CLANG_LLD", "True")
        # set number of concurrent build jobs
        env.set("MAX_JOBS", make_jobs)
        # add a directory for triton's downloads
        triton_home = f"{self.build_directory}/.triton_home"
        env.set("TRITON_HOME", triton_home)
        # use spack installed dependencies
        env.set("PYBIND11_SYSPATH", self.spec["py-pybind11"].prefix)
        env.set("TRITON_PTXAS_PATH", self.spec["cuda"].prefix)
        env.set("TRITON_CUOBJDUMP_PATH", self.spec["cuda"].prefix)
        env.set("TRITON_NVDISASM_PATH", self.spec["cuda"].prefix)
        env.set("TRITON_CUDACRT_PATH", self.spec["cuda"].prefix)
        env.set("TRITON_CUDART_PATH", self.spec["cuda"].prefix)
        cupti_path = self.spec["cuda"].prefix.extras.CUPTI
        env.set("TRITON_CUPTI_INCLUDE_PATH", f"{cupti_path}/include")
        env.set("TRITON_CUPTI_LIB_PATH", f"{cupti_path}/lib64")

    # build_directory does not work since apparently one needs to call pip from
    # the parent directory
    # build_directory = "python"


# override pip install to use python subdirectory from parent directory
class PythonPipBuilder(build_systems.python.PythonPipBuilder):
    def install(self, pkg: PythonPackage, spec: Spec, prefix: Prefix) -> None:
        pip = spec["python"].command
        pip.add_default_arg("-m", "pip")
        args = build_systems.python.PythonPipBuilder.std_args(pkg) + [f"--prefix={prefix}"]
        # build directory specified manually as additional argument to pip install
        args.append("./python")
        with fs.working_dir(self.build_directory):
            pip(*args)
