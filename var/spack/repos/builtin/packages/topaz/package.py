# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Topaz(PythonPackage):
    """topaz: Pipeline for particle picking in cryo-electron microscopy images using
    convolutional neural networks trained from positive and unlabeled examples. Also
    featuring micrograph and tomogram denoising with DNNs."""

    homepage = "https://topaz-em.readthedocs.io/"
    pypi = "topaz-em/topaz_em-0.2.5.tar.gz"

    license("GPL-3.0-or-later")

    version("0.3.7", sha256="ae3c0d6ccb1e8ad2e4926421442b8cb33a4d01d1ee1dff83174949a9f91cc8a9")
    version("0.2.5", sha256="002a6eb775598b6c4df0225f3a488bfe6a6da9246e8ca42eb4e7d58f694c25cc")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1:2.3.1", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-numpy@1.11:", type=("build", "run"))
    depends_on("py-pandas@0.20.3:", type=("build", "run"))
    depends_on("py-scikit-learn@0.19.0:", type=("build", "run"))
    depends_on("py-scipy@0.17.0:", type=("build", "run"))
    depends_on("py-pillow@6.2.0:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-tqdm@4.65.0:", type=("build", "run"), when="@0.3.7:")
    depends_on("py-h5py@3.7.0:", type=("build", "run"), when="@0.3.7:")
