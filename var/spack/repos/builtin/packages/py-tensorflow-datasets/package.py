# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorflowDatasets(PythonPackage):
    """tensorflow/datasets is a library of datasets ready to use with
    TensorFlow."""

    homepage = "https://github.com/tensorflow/datasets"
    pypi = "tensorflow-datasets/tensorflow-datasets-4.4.0.tar.gz"

    license("Apache-2.0")

    version("4.4.0", sha256="3e95a61dec1fdb7b05dabc0dbed1b531e13d6c6fd362411423d0a775e5e9b960")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py", type=("build", "run"))
    depends_on("py-attrs@18.1.0:", type=("build", "run"))
    depends_on("py-dill", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-promise", type=("build", "run"))
    depends_on("py-protobuf@3.12.2:", type=("build", "run"))
    depends_on("py-requests@2.19.0:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-tensorflow-metadata", type=("build", "run"))
    depends_on("py-termcolor", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"), when="^python@:3.7")
    depends_on("py-importlib-resources", type=("build", "run"), when="^python@:3.8")
