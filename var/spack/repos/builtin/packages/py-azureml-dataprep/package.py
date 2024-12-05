# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlDataprep(PythonPackage):
    """Azure ML Data Preparation SDK."""

    homepage = "https://docs.microsoft.com/en-us/python/api/overview/azure/ml/?view=azure-ml-py"
    url = "https://pypi.io/packages/py3/a/azureml_dataprep/azureml_dataprep-2.0.2-py3-none-any.whl"

    version("2.11.0", sha256="755c0d7cfe228705aee7adc97813fb6d7d6ecb048b66f47c1fd5897f2709c3a2")
    version("2.10.1", sha256="a36f807112ff1e64d21265b8e7f40154c93e3bead539e2a74c9d74200fd77c86")

    variant("fuse", default=False, description="Build with FUSE support")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-dotnetcore2@2.1.14:2", type=("build", "run"))
    depends_on("py-azureml-dataprep-native@30.0.0:30", when="@2.10.0:", type=("build", "run"))
    depends_on("py-azureml-dataprep-rslex@1.9.0:1.9", when="@2.11.0:", type=("build", "run"))
    depends_on("py-azureml-dataprep-rslex@1.8.0:1.8", when="@2.10.1", type=("build", "run"))
    depends_on("py-cloudpickle@1.1.0:1", type=("build", "run"))
    depends_on("py-azure-identity@1.2.0:1.4", when="@2.10.0:", type=("build", "run"))
    depends_on("py-fusepy@3.0.1:3", when="+fuse", type=("build", "run"))
