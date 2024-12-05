# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySkl2onnx(PythonPackage):
    """Convert scikit-learn models to ONNX"""

    homepage = "https://github.com/onnx/sklearn-onnx"
    pypi = "skl2onnx/skl2onnx-1.10.3.tar.gz"

    license("Apache-2.0")

    version("1.12", sha256="15f4a07b97f7c5bf11b7353b8cb75c9f8c161485deb198cb49cc61a9d507c29c")
    version("1.10.3", sha256="798933378145412b9876ab3ff2c1dd5f241a7296406d786262000afa8d329628")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.15:", type=("build", "run"))
    depends_on("py-scipy@1.0:", type=("build", "run"))
    depends_on("py-protobuf", type=("build", "run"))
    depends_on("py-onnx@1.2.1:", type=("build", "run"))
    depends_on("py-scikit-learn@0.19:1.1.1", type=("build", "run"))
    depends_on("py-onnxconverter-common@1.7.0:", type=("build", "run"))
    # Although this dep is undocumented, it's imported at run-time.
    depends_on("py-packaging", when="@1.12:", type=("build", "run"))
