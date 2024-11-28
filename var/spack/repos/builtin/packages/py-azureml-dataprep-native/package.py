# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyAzuremlDataprepNative(PythonPackage):
    """Python Package for AzureML DataPrep specific native extensions."""

    homepage = "https://docs.microsoft.com/en-us/python/api/overview/azure/ml/?view=azure-ml-py"

    skip_version_audit = ["platform=windows"]

    if sys.platform == "darwin":
        version(
            "30.0.0-py3.9",
            sha256="eaf3fcd9f965e87b03fe89d7c6fe6abce53483a79afc963e4981061f4c250e85",
            url="https://pypi.io/packages/cp39/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp39-cp39-macosx_10_9_x86_64.whl",
        )
        version(
            "30.0.0-py3.8",
            sha256="6772b638f9d03a041b17ce4343061f5d543019200904b9d361b2b2629c3595a7",
            preferred=True,
            url="https://pypi.io/packages/cp38/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp38-cp38-macosx_10_9_x86_64.whl",
        )
    elif sys.platform.startswith("linux"):
        version(
            "30.0.0-py3.9",
            sha256="b8673136948f682c84d047feacbfee436df053cba4f386f31c4c3a245a4e3646",
            url="https://pypi.io/packages/cp39/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp39-cp39-manylinux1_x86_64.whl",
        )
        version(
            "30.0.0-py3.8",
            sha256="d07cf20f22b14c98576e135bbad9bb8aaa3108941d2beaadf050b4238bc93a18",
            preferred=True,
            url="https://pypi.io/packages/cp38/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp38-cp38-manylinux1_x86_64.whl",
        )

    depends_on("python@3.9.0:3.9", when="@30.0.0-py3.9", type=("build", "run"))
    depends_on("python@3.8.0:3.8", when="@30.0.0-py3.8", type=("build", "run"))
