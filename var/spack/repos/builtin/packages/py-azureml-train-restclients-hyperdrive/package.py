# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlTrainRestclientsHyperdrive(PythonPackage):
    """The azureml-train-restclients-hyperdrive contains functionality for
    azureml-train metapackage."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_train_restclients_hyperdrive/azureml_train_restclients_hyperdrive-1.11.0-py3-none-any.whl"

    version("1.23.0", sha256="8ecee0cdb92a4a431b778ebcc7f9fe7c5bf63ea4cae9caa687980bc34ae3a42c")
    version("1.11.0", sha256="8bc6f9676a9f75e6ee06d201c418ea904c24e854f26cf799b08c259c3ac92d13")
    version("1.8.0", sha256="1633c7eb0fd96714f54f72072ccf1c5ee1ef0a8ba52680793f20d27e0fd43c87")

    depends_on("python@3.5:3", type=("build", "run"))
    depends_on("py-requests@2.19.1:", type=("build", "run"))
    depends_on("py-msrest@0.5.1:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.33:", type=("build", "run"))
