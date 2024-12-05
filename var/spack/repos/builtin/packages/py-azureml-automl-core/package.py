# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlAutomlCore(PythonPackage):
    """The azureml-automl-core package is a package containing functionality
    used by the azureml-train-automl package."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_automl_core/azureml_automl_core-1.11.0-py3-none-any.whl"

    version("1.23.0", sha256="1fa4a900856b15e1ec9a6bb949946ed0c873a5a54da3db592f03dbb46a117ceb")

    depends_on("python@3.5:3", type=("build", "run"))

    depends_on("py-azureml-dataset-runtime@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
    depends_on("py-azureml-telemetry@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
