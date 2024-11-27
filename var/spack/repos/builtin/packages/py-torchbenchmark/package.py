# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchbenchmark(Package):
    """A collection of open source benchmarks used to evaluate PyTorch performance."""

    homepage = "https://github.com/pytorch/benchmark"
    git = "https://github.com/pytorch/benchmark.git"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version("main", branch="main")

    # README.md
    depends_on("python@3.8:+pythoncmd", type=("build", "run"))
    depends_on("git-lfs", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-torchaudio", type=("build", "run"))
    depends_on("py-torchtext", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))

    # requirements.txt
    depends_on("py-accelerate", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-patch", type=("build", "run"))
    depends_on("py-py-cpuinfo", type=("build", "run"))
    depends_on("py-distro", type=("build", "run"))
    depends_on("py-iopath", type=("build", "run"))
    depends_on("py-pytest", type=("build", "run"))
    depends_on("py-pytest-benchmark", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-timm", type=("build", "run"))
    depends_on("py-transformers", type=("build", "run"))
    depends_on("py-monkeytype", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-kornia", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-submitit", type=("build", "run"))

    # torchbenchmark/models/BERT_pytorch/setup.py
    depends_on("py-setuptools", type="build")

    def patch(self):
        # Avoid attempts to install dependencies
        filter_file(r" = pip_install_requirements\(.*\)", " = True, 'skip'", "install.py")
        filter_file(
            r" = _install_deps\(.*\)",
            " = (True, None, None)",
            join_path("torchbenchmark", "__init__.py"),
        )

    def install(self, spec, prefix):
        # Downloads datasets and models
        python("install.py", "--verbose")

        # Copy to installation prefix
        install_tree(".", prefix)
