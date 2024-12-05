# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCtgan(PythonPackage):
    """CTGAN is a collection of Deep Learning based Synthetic
    Data Generators for single table data, which are able to
    learn from real data and generate synthetic clones with
    high fidelity."""

    homepage = "https://github.com/sdv-dev/CTGAN"
    pypi = "ctgan/ctgan-0.5.0.tar.gz"

    license("MIT")

    version("0.5.0", sha256="b8a5dbf21dab2d2e2690013f13feb0922f5bad13440b15bc031ce9d58c7fb988")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-packaging@20:21", type=("build", "run"))
    depends_on("py-numpy@1.20:1", type=("build", "run"))
    depends_on("py-pandas@1.1.3:1", type=("build", "run"))
    depends_on("py-scikit-learn@0.24:1", type=("build", "run"))
    depends_on("py-torch@1.8.0:1", type=("build", "run"))
    depends_on("py-torchvision@0.9:0", type=("build", "run"))
    depends_on("py-rdt@0.6.1:0.6", type=("build", "run"))
