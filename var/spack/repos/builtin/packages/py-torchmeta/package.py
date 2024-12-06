# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchmeta(PythonPackage):
    """A collection of extensions and data-loaders for few-shot learning &
    meta-learning in PyTorch. Torchmeta contains popular meta-learning
    benchmarks, fully compatible with both torchvision and PyTorch's DataLoader."""

    homepage = "https://github.com/tristandeleu/pytorch-meta"
    pypi = "torchmeta/torchmeta-1.7.0.tar.gz"

    license("MIT")

    version("1.7.0", sha256="148d42b6a1ec27970408f7bcb97cf1cb203f8699214e06424fe43d78faa848d9")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.14:", type=("build", "run"))
    depends_on("py-torch@1.4.0:1.8", type=("build", "run"))
    depends_on("py-torchvision@0.5.0:0.9", type=("build", "run"))
    depends_on("pil@7.0:", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-tqdm@4.0.0:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-ordered-set", type=("build", "run"))
