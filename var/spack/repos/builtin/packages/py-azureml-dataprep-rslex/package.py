# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import archspec

from spack.package import *


class PyAzuremlDataprepRslex(PythonPackage):
    """Azure Machine Learning Data Prep RsLex is a Rust implementation of Data Prep's
    capabilities to load, transform, and write data for machine learning workflows."""

    homepage = "https://docs.microsoft.com/en-us/python/api/overview/azure/ml/?view=azure-ml-py"

    skip_version_audit = ["platform=windows"]

    if sys.platform == "darwin":
        version(
            "1.9.0-py3.9",
            sha256="9bdaa31d129dac19ee20d5a3aad1726397e90d8d741b4f6de4554040800fefe8",
            url="https://pypi.io/packages/cp39/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp39-cp39-macosx_10_9_x86_64.whl",
        )
        version(
            "1.9.0-py3.8",
            sha256="9b2e741ac1c53d3f7e6061d264feccf157d97e404c772933a176e6021014484e",
            preferred=True,
            url="https://pypi.io/packages/cp38/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp38-cp38-macosx_10_9_x86_64.whl",
        )

        version(
            "1.8.0-py3.9",
            sha256="677c25a7e23ec7f91d25aa596f382f7f3b6d60fbc3258bead2b2a6aa42f3a16d",
            url="https://pypi.io/packages/cp39/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp39-cp39-macosx_10_9_x86_64.whl",
        )
        version(
            "1.8.0-py3.8",
            sha256="d7f2dec06296544b1707f5b01c6a4eaad744b4abfe9e8e89830b561c84d95a7a",
            url="https://pypi.io/packages/cp38/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp38-cp38-macosx_10_9_x86_64.whl",
        )
    elif sys.platform.startswith("linux"):
        version(
            "1.9.0-py3.9",
            sha256="79d52bb427e3ca781a645c4f11f7a8e5e2c8f61e61bfc162b4062d8e47bcf3d6",
            url="https://pypi.io/packages/cp39/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp39-cp39-manylinux1_x86_64.whl",
        )
        version(
            "1.9.0-py3.8",
            sha256="a52461103b45867dd919bab593bb6f2426c9b5f5a435081e82a3c57c54c3add6",
            preferred=True,
            url="https://pypi.io/packages/cp38/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp38-cp38-manylinux1_x86_64.whl",
        )

        version(
            "1.8.0-py3.9",
            sha256="e251a077669703ca117b157b225fbc20832169f913476cf79c01a5c6f8ff7a50",
            url="https://pypi.io/packages/cp39/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp39-cp39-manylinux1_x86_64.whl",
        )
        version(
            "1.8.0-py3.8",
            sha256="2ebfa164f0933a5cec383cd27ba10d33861a73237ef481ada5a9a822bb55514a",
            url="https://pypi.io/packages/cp38/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp38-cp38-manylinux1_x86_64.whl",
        )

    depends_on("python@3.9.0:3.9", when="@1.9.0-py3.9,1.8.0-py3.9", type=("build", "run"))
    depends_on("python@3.8.0:3.8", when="@1.9.0-py3.8,1.8.0-py3.8", type=("build", "run"))

    for t in set(
        [str(x.family) for x in archspec.cpu.TARGETS.values() if str(x.family) != "x86_64"]
    ):
        conflicts(
            "target={0}:".format(t), msg="py-azureml-dataprep-rslex is available x86_64 only"
        )
