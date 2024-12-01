# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOnnxOpcounter(PythonPackage):
    """ONNX flops / params counter."""

    homepage = "https://github.com/gmalivenko/onnx-opcounter"
    pypi = "onnx_opcounter/onnx_opcounter-0.0.3.tar.gz"

    license("Apache-2.0")

    version("0.0.3", sha256="c75e76d066eb777e4855c486beb402b1fef83783a6634237b8ca20eb75cce8c9")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-numpy")
        depends_on("py-onnx")
        depends_on("py-onnxruntime")
