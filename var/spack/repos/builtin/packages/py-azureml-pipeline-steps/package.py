# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlPipelineSteps(PythonPackage):
    """Represents a unit of computation in azureml-pipeline."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_pipeline_steps/azureml_pipeline_steps-1.11.0-py3-none-any.whl"

    version("1.23.0", sha256="72154c2f75624a1e7500b8e2239ae1354eeedf66d2cabb11e213b7eb80aedddb")

    depends_on("python@3:", type=("build", "run"))

    depends_on("py-azureml-train-core@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
    depends_on("py-azureml-train-automl-client@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
    depends_on("py-azureml-pipeline-core@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
