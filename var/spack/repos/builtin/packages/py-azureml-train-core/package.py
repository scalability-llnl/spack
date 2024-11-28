# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlTrainCore(PythonPackage):
    """The azureml-train-core contains functionality used by azureml-train
    metapackage."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_train_core/azureml_train_core-1.11.0-py3-none-any.whl"

    version("1.23.0", sha256="5c384ea0bea3ecd8bf2a1832dda906fd183cf2a03ad3372cb824ce8fa417979e")
    version("1.11.0", sha256="1b5fd813d21e75cd522d3a078eba779333980a309bcff6fc72b74ddc8e7a26f1")
    version("1.8.0", sha256="5a8d90a08d4477527049d793feb40d07dc32fafc0e4e57b4f0729d3c50b408a2")

    depends_on("python@3.5:3", type=("build", "run"))

    depends_on(
        "py-azureml-train-restclients-hyperdrive@1.23.0:1.23",
        when="@1.23.0",
        type=("build", "run"),
    )
    depends_on("py-azureml-core@1.23.0:1.23", when="@1.23.0", type=("build", "run"))
    depends_on("py-azureml-telemetry@1.23.0:1.23", when="@1.23.0", type=("build", "run"))

    depends_on(
        "py-azureml-train-restclients-hyperdrive@1.11.0:1.11",
        when="@1.11.0",
        type=("build", "run"),
    )
    depends_on("py-azureml-core@1.11.0:1.11", when="@1.11.0", type=("build", "run"))
    depends_on("py-azureml-telemetry@1.11.0:1.11", when="@1.11.0", type=("build", "run"))

    depends_on(
        "py-azureml-train-restclients-hyperdrive@1.8.0:1.8", when="@1.8.0", type=("build", "run")
    )
    depends_on("py-azureml-core@1.8.0:1.8", when="@1.8.0", type=("build", "run"))
    depends_on("py-azureml-telemetry@1.8.0:1.8", when="@1.8.0", type=("build", "run"))
    depends_on("py-flake8@3.1.0:3.7.9", when="@1.8.0 ^python@3.6:", type=("build", "run"))
