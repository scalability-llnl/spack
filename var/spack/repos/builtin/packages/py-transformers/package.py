# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTransformers(PythonPackage):
    """State-of-the-art Natural Language Processing for TensorFlow 2.0 and
    PyTorch"""

    homepage = "https://github.com/huggingface/transformers"
    pypi = "transformers/transformers-2.8.0.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("4.42.3", sha256="7539873ff45809145265cbc94ea4619d2713c41ceaa277b692d8b0be3430f7eb")
    version("4.38.1", sha256="86dc84ccbe36123647e84cbd50fc31618c109a41e6be92514b064ab55bf1304c")
    version("4.35.2", sha256="2d125e197d77b0cdb6c9201df9fa7e2101493272e448b9fba9341c695bee2f52")
    version("4.31.0", sha256="4302fba920a1c24d3a429a29efff6a63eac03f3f3cf55b55927fc795d01cb273")
    version("4.24.0", sha256="486f353a8e594002e48be0e2aba723d96eda839e63bfe274702a4b5eda85559b")
    version("4.6.1", sha256="83dbff763b7e7dc57cbef1a6b849655d4fcab6bffdd955c5e8bea12a4f76dc10")
    version("2.8.0", sha256="b9f29cdfd39c28f29e0806c321270dea337d6174a7aa60daf9625bf83dbb12ee")

    depends_on("cxx", type="build")  # generated

    with default_args(type="build"):
        depends_on("py-setuptools")

    with default_args(type=("build", "run")):
        depends_on("py-filelock")
        depends_on("py-huggingface-hub@0.23.2:", when="@4.42.3:")
        depends_on("py-huggingface-hub@0.19.3:", when="@4.38.1:")
        depends_on("py-huggingface-hub@0.16.4:0", when="@4.34:")
        depends_on("py-huggingface-hub@0.14.1:0", when="@4.26:")
        depends_on("py-huggingface-hub@0.10:0", when="@4.24:")
        depends_on("py-huggingface-hub@0.0.8", when="@4.6.1")
        depends_on("py-numpy@1.17:1", when="@4.6:")
        depends_on("py-numpy@:1")
        depends_on("py-packaging@20:", when="@4.24:")
        depends_on("py-packaging", when="@4.6.1")
        depends_on("py-pyyaml@5.1:", when="@4.24:")
        depends_on("py-regex@:2019.12.16,2019.12.18:")
        depends_on("py-requests")
        depends_on("py-safetensors@0.4.1:", when="@4.38.1:")
        depends_on("py-safetensors@0.3.1:", when="@4.31:")
        depends_on("py-tokenizers@0.19", when="@4.40.0:")
        depends_on("py-tokenizers@0.14:0.18", when="@4.35:4.39.3")
        depends_on("py-tokenizers@0.11.1:0.11.2,0.11.4:0.13", when="@4.24:4.33")
        depends_on("py-tokenizers@0.10.1:0.10", when="@4.6.1")
        depends_on("py-tokenizers@0.5.2", when="@2.8.0")
        depends_on("py-tqdm@4.27:")

        # Historical requirements
        depends_on("py-sacremoses", when="@:4.6")
        depends_on("py-boto3", when="@2.8.0")
        depends_on("py-sentencepiece", when="@2.8.0")
