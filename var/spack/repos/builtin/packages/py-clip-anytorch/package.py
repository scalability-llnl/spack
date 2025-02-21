# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyClipAnytorch(PythonPackage):
    """CLIP (Contrastive Language-Image Pre-Training) is a neural network
    trained on a variety of (image, text) pairs. It can be instructed in
    natural language to predict the most relevant text snippet, given an image,
    without directly optimizing for the task, similarly to the zero-shot
    capabilities of GPT-2 and 3. We found CLIP matches the performance of the
    original ResNet50 on ImageNet "zero-shot" without using any of the original
    1.28M labeled examples, overcoming several major challenges in computer
    vision."""

    homepage = "https://github.com/rom1504/CLIP"
    # PyPI source is missing requirements.txt
    url = "https://github.com/rom1504/CLIP/archive/refs/tags/2.6.0.tar.gz"

    license("MIT", checked_by="qwertos")

    version("2.6.0", sha256="1ac1f6ca47dfb5d4e55be8f45cc2f3bdf6415b91973a04b4529e812a8ae29bea")

    depends_on("py-setuptools", type="build")
    depends_on("py-ftfy", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
