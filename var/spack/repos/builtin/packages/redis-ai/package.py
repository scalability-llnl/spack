# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class RedisAi(MakefilePackage):
    """A Redis module for serving tensors and executing deep learning graphs"""

    homepage = "https://oss.redis.com/redisai/"
    git = "https://github.com/RedisAI/RedisAI.git"

    maintainers("MattToast")

    license("Apache-2.0")

    version(
        "1.2.7", tag="v1.2.7", commit="1bf38d86233ba06e1350ca9de794df2b07cdb274", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("torch", default=True, description="Build with the pytorch backend")
    variant("cuda", default=False, description="Use CUDA")
    variant("rocm", default=False, description="Use ROCm")

    conflicts("+cuda+rocm")

    # Required dependencies
    depends_on("git", type=("build", "link"))
    depends_on("git-lfs", type=("build", "link"))
    depends_on("python@3:", type=("build", "link"))
    depends_on("py-pip", type=("build", "link"))
    depends_on("cmake@3.0:", type=("build", "link"))
    depends_on("gmake", type=("build", "link"))

    # GPU deps
    depends_on("cuda@11.2:", type=("build", "link", "run"), when="+cuda")
    depends_on("cudnn@8.1:", type=("build", "link", "run"), when="+cuda")

    with when("+rocm"):
        depends_on("hsa-rocr-dev")
        depends_on("hip")
        depends_on("rocprim")
        depends_on("hipcub")
        depends_on("rocthrust")
        depends_on("roctracer-dev")
        depends_on("rocrand")
        depends_on("hipsparse")
        depends_on("hipfft")
        depends_on("rocfft")
        depends_on("rocblas")
        depends_on("miopen-hip")
        depends_on("rocminfo")

    # Optional Deps
    with when("+torch"):
        depends_on("py-torch@1.11.0:~cuda~rocm", type=("build", "link"), when="~cuda~rocm")
        depends_on("py-torch@1.11.0:+cuda+cudnn~rocm", type=("build", "link"), when="+cuda")
        depends_on("py-torch@1.11.0:~cuda+rocm", type=("build", "link"), when="+rocm")

    build_directory = "opt"
    parallel = False

    @property
    def use_gpu(self):
        return self.spec.satisfies("+cuda") or self.spec.satisfies("+rocm")

    @property
    def with_torch(self):
        return self.spec.satisfies("+torch")

    @property
    def torch_dir(self):
        return (
            join_path(self.spec["py-torch"].package.cmake_prefix_paths[0], "Torch")
            if self.with_torch
            else None
        )

    @property
    def build_env(self):
        build_env = {
            "WITH_TF": "0",
            "WITH_TFLITE": "0",
            "WITH_PT": "0",
            "WITH_ORT": "0",
            "WITH_UNIT_TESTS": "0",
            "GPU": "1" if self.use_gpu else "0",
        }
        if self.with_torch:
            build_env["WITH_PT"] = "1"
            build_env["Torch_DIR"] = self.torch_dir
        return build_env

    def edit(self, spec, prefix):
        # resolve deps not provided through spack
        Executable(join_path(".", "get_deps.sh"))(
            extra_env={
                "VERBOSE": "1",
                # Need to grab the RAI specific version of dlpack
                "WITH_DLPACK": "1",
                # Do not get ml backends, they should be retrieved through spack
                "WITH_TF": "0",
                "WITH_TFLITE": "0",
                "WITH_PT": "0",
                "WITH_ORT": "0",
                # Decide if we want GPU
                "GPU": "1" if self.use_gpu else "0",
            }
        )
        env.update(self.build_env)

    def install(self, spec, prefix):
        super(RedisAi, self).install(spec, prefix)
        install_tree("install-*", prefix)

    @run_after("install")
    @on_package_attributes(with_torch=True)
    def copy_libtorch(self):
        torch_site_dir = os.path.dirname(os.path.dirname(os.path.dirname(self.torch_dir)))
        torch_lib_dir = join_path(torch_site_dir, "lib")
        install_tree(torch_lib_dir, self.prefix.backends.redisai_torch.lib)

    def setup_run_environment(self, env):
        env.set("REDIS_AI", self.prefix.join("redisai.so"))
