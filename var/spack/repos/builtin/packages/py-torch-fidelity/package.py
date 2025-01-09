# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyTorchFidelity(PythonPackage):
    """High-fidelity performance metrics for generative models in PyTorch"""

    homepage = "https://www.github.com/toshas/torch-fidelity"
    pypi = "torch_fidelity/torch_fidelity-0.3.0.tar.gz"

    license("Apache-2.0", checked_by="qwertos")

    version("0.3.0", sha256="3d3e33db98919759cc4f3f24cb27e1e74bdc7c905d90a780630e4e1c18492b66")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))

    def patch(self):
        os.rename(
            join_path(self.stage.source_path, "torch_fidelity.egg-info", "requires.txt"),
            join_path(self.stage.source_path, "requirements.txt"),
        )
