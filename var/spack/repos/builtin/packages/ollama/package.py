# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.go
from spack.package import *


class Ollama(GoPackage, CudaPackage):
    """Run Llama 2, Code Llama, and other models. Customize and create your own."""

    homepage = "https://ollama.com"
    git = "https://github.com/ollama/ollama.git"

    maintainers("teaguesterling", "brettviren")

    # A shell script is run by `go generate` which assumes source is in a git
    # repo.  So we must use git VCS and not tarballs and defeat source caching.
    with default_args(submodules=True, no_cache=True):
        version("0.3.9", commit="a1cef4d0a5f31280ea82b350605775931a6163cb")
        version("0.1.31", commit="dc011d16b9ff160c0be3829fc39a43054f0315d0")
        # This is the last verified non-preview version as of 20240413
        version("0.1.30", commit="756c2575535641f1b96d94b4214941b90f4c30c7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    license("MIT", checked_by="teaguesterling")

    depends_on("cmake@3.24:", type="build")
    depends_on("go@1.4.0:", type="build")
    depends_on("git", type="build")


class GoBuilder(spack.build_systems.go.GoBuilder):
    phases = ("generate", "build", "install")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+cuda"):
            # These variables are consumed by gen_linux.sh which is called by
            # "go generate".
            cuda_prefix = self.spec["cuda"].prefix
            env.set("CUDACXX", cuda_prefix.bin.nvcc)
            env.set("CUDA_LIB_DIR", cuda_prefix.lib)
            env.set("CMAKE_CUDA_ARCHITECTURES", spec.variants["cuda_arch"].value)

    @property
    def generate_args(self):
        """Arguments for ``go generate``."""
        return ["./..."]

    def generate(self, pkg, spec, prefix):
        """Runs ``go generate`` in the source directory"""
        with working_dir(self.build_directory):
            go("generate", *self.generate_args)
