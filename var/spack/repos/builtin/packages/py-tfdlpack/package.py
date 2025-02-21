# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyTfdlpack(CMakePackage, PythonExtension):
    """Tensorflow plugin for DLPack."""

    homepage = "https://github.com/VoVAllen/tf-dlpack"
    git = "https://github.com/VoVAllen/tf-dlpack.git"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("master", branch="master", submodules=True)
    version(
        "0.1.1", tag="v0.1.1", commit="a1fdb53096158c2ec9189bb1ff46c92c6f571bbe", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cuda", default=True, description="Build with CUDA support")

    depends_on("cmake@3.5:", type="build")
    depends_on("cuda", when="+cuda")

    # Python dependencies
    extends("python")
    depends_on("py-setuptools", type="build")
    depends_on("py-tensorflow", type=("build", "run"))

    def cmake_args(self):
        return [self.define_from_variant("USE_CUDA", "cuda")]

    def install(self, spec, prefix):
        with working_dir("python"):
            pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")

    def setup_run_environment(self, env):
        # Prevent TensorFlow from taking over the whole GPU
        env.set("TF_FORCE_GPU_ALLOW_GROWTH", "true")
