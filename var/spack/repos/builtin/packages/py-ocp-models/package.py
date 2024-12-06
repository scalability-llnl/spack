# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyOcpModels(PythonPackage):
    """Reference implementation for the MLPerf HPC OpenCatalyst DimeNet++ benchmark"""

    homepage = "https://opencatalystproject.org/"
    git = "https://github.com/mlcommons/hpc.git"

    version("main", branch="main")

    tags = ["proxy-app"]

    depends_on("python@3.8", type=("build", "run"))
    depends_on("py-ase@3.21", type=("build", "run"))
    depends_on("py-matplotlib@3.3", type=("build", "run"))
    depends_on("py-pre-commit@2.10", type=("build", "run"))
    depends_on("py-pymatgen@2020.12.31", type=("build", "run"))
    depends_on("py-torch@1.8.1", type=("build", "run"))
    depends_on("py-pyyaml@5.4", type=("build", "run"))
    depends_on("py-tensorboard@2.4", type=("build", "run"))
    depends_on("py-tqdm@4.58", type=("build", "run"))
    depends_on("py-sphinx", type=("build", "run"))
    depends_on("py-nbsphinx", type=("build", "run"))
    depends_on("pandoc", type=("build", "run"))
    depends_on("py-black", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-torch-scatter", type=("build", "run"))
    depends_on("py-torch-cluster", type=("build", "run"))
    depends_on("py-torch-sparse", type=("build", "run"))
    depends_on("py-torch-spline-conv", type=("build", "run"))
    depends_on("py-demjson", type=("build", "run"))
    depends_on("py-pillow", type=("build", "run"))
    depends_on("py-torch-geometric", type=("build", "run"))
    depends_on("py-wandb", type=("build", "run"))
    depends_on("py-lmdb@1.1.1", type=("build", "run"))
    depends_on("py-pytest@6.2.2", type=("build", "run"))
    depends_on("py-submitit", type=("build", "run"))
    depends_on("py-sphinx-rtd-theme", type=("build", "run"))

    build_directory = "open_catalyst"
