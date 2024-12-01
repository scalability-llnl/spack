# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchGeometric(PythonPackage):
    """Graph Neural Network Library for PyTorch."""

    homepage = "https://pyg.org/"
    pypi = "torch-geometric/torch_geometric-2.5.3.tar.gz"
    git = "https://github.com/pyg-team/pytorch_geometric.git"

    license("MIT")
    maintainers("adamjstewart")

    version("2.5.3", sha256="ad0761650c8fa56cdc46ee61c564fd4995f07f079965fe732b3a76d109fd3edc")

    depends_on("py-flit-core@3.2:3", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-tqdm")
        depends_on("py-numpy")
        depends_on("py-scipy")
        depends_on("py-fsspec")
        depends_on("py-jinja2")
        depends_on("py-aiohttp")
        depends_on("py-requests")
        depends_on("py-pyparsing")
        depends_on("py-scikit-learn")
        depends_on("py-psutil@5.8:")

        # Undocumented dependencies
        depends_on("py-torch")
