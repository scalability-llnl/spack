# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlTrainAutomlClient(PythonPackage):
    """The azureml-train-automl-client package contains functionality for
    automatically finding the best machine learning model and its parameters,
    given training and test data."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_train_automl_client/azureml_train_automl_client-1.11.0-py3-none-any.whl"

    version("1.23.0", sha256="ac5f1ce9b04b4e61e2e28e0fa8d2d8e47937a546f624d1cd3aa6bc4f9110ecbe")

    depends_on("python@3.5:3", type=("build", "run"))

    depends_on("py-azureml-automl-core@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
    depends_on("py-azureml-core@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
    depends_on("py-azureml-dataset-runtime@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
    depends_on("py-azureml-telemetry@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
