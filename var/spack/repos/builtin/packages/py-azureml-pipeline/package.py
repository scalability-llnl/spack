# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlPipeline(PythonPackage):
    """The Azure Machine Learning SDK for Python can be used to create ML
    pipelines as well as to submit and track individual pipeline runs."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = (
        "https://pypi.io/packages/py3/a/azureml_pipeline/azureml_pipeline-1.11.0-py3-none-any.whl"
    )

    version("1.23.0", sha256="ed0fae96771840d3ffd63d63df1b1eed2f50c3b8dbe7b672a4f1ba6e66d0a392")

    depends_on("python@3:", type=("build", "run"))

    depends_on("py-azureml-pipeline-core@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
    depends_on("py-azureml-pipeline-steps@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
