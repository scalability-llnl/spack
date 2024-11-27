# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVectorQuantizePytorch(PythonPackage):
    """A vector quantization library originally transcribed
    from Deepmind's tensorflow implementation, made
    conveniently into a package. It uses exponential moving
    averages to update the dictionary."""

    homepage = "https://github.com/lucidrains/vector-quantize-pytorch"
    pypi = "vector_quantize_pytorch/vector_quantize_pytorch-0.3.9.tar.gz"

    license("MIT")

    version("0.3.9", sha256="783ca76251299f0e3eb244062bc05c4416bb29157e57077e4a8969c5277f05ee")

    depends_on("py-setuptools", type="build")
    depends_on("py-einops", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
