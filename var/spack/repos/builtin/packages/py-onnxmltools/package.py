# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOnnxmltools(PythonPackage):
    """Converts Machine Learning models to ONNX"""

    homepage = "https://github.com/onnx/onnxmltools"
    pypi = "onnxmltools/onnxmltools-1.10.0.tar.gz"

    license("Apache-2.0")

    # Source tarball not available on PyPI
    version(
        "1.11.1",
        url="https://github.com/onnx/onnxmltools/archive/1.11.1.tar.gz",
        sha256="a739dc2147a2609eff2b2aad4a423b9795a49557c6b4c55b15c9ee323b4a01b7",
    )

    version("1.11.0", sha256="174b857edcc2e4c56adbc7aed5234fff6a0f51a45956eb4c05c9f842c98bfa1f")
    version("1.10.0", sha256="4eb4605f18ed66553fc17438ac8cf5406d66dcc624bedd76d8067e1b08e6c75d")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-onnx", type=("build", "run"))
    depends_on("py-skl2onnx", type=("build", "run"))
    depends_on("py-onnxruntime", type=("build", "run"))
