# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNanotron(PythonPackage):
    """Minimalistic large language model 3D-parallelism training."""

    homepage = "https://github.com/huggingface/nanotron"
    url = "https://github.com/huggingface/nanotron/archive/refs/tags/v0.4.tar.gz"
    git = "https://github.com/huggingface/nanotron.git"

    maintainers("thomas-bouvier")

    license("Apache-2.0")

    version("main", branch="main")
    version("0.4", sha256="7ea378eb1b6b16c93a3021fcfd71dd73bd14d826126eae215e2b02e05cd6a120")

    depends_on("python@3.6:3.11")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.13.0:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-numpy@:2", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-safetensors", type=("build", "run"))
    depends_on("py-dacite", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-datasets", type=("build", "run"), when="@0.5:")
