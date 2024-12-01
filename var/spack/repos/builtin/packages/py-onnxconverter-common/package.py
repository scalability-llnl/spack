# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOnnxconverterCommon(PythonPackage):
    """ONNX Converter and Optimization Tools"""

    homepage = "https://github.com/microsoft/onnxconverter-common"
    url = "https://github.com/microsoft/onnxconverter-common/archive/refs/tags/v1.9.0.tar.gz"

    license("MIT")

    version("1.9.0", sha256="32315bcc844a8203092f3117a4a092ac6cf03d6a20145477e284f1172557d6f9")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-protobuf", type=("build", "run"))
    depends_on("py-onnx", type=("build", "run"))
