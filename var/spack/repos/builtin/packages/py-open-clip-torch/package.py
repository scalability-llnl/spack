# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOpenClipTorch(PythonPackage):
    """Welcome to an open source implementation of OpenAI's CLIP (Contrastive
    Language-Image Pre-training)."""

    homepage = "https://github.com/mlfoundations/open_clip"
    url = "https://github.com/mlfoundations/open_clip/archive/refs/tags/v2.24.0.tar.gz"

    license("MIT", checked_by="alex391")

    version("2.24.0", sha256="83d78a78f756685e80fdb8baa2f2fb308c791fabdbfe1c0ddcd6fed7d22de7b6")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.9.0:", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-ftfy", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-huggingface-hub", type=("build", "run"))
    depends_on("py-sentencepiece", type=("build", "run"))
    depends_on("py-protobuf", type=("build", "run"))
    depends_on("py-timm", type=("build", "run"))
