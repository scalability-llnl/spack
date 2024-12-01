# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeras2onnx(PythonPackage):
    """Converts Machine Learning models to ONNX for use in Windows ML"""

    homepage = "https://github.com/onnx/keras-onnx"

    url = "https://github.com/onnx/keras-onnx/archive/refs/tags/v1.7.0.tar.gz"

    license("MIT")

    version("1.7.0", sha256="8ec9c4e1c1f870d420934d1aa7cbc9faab80c6af366900bf95e5f48280c0d199")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-protobuf", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-onnx", type=("build", "run"))
    depends_on("py-onnxconverter-common@1.7.0:", type=("build", "run"))
    depends_on("py-fire", type=("build", "run"))
