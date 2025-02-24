# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginAzureBatch(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to Microsoft Azure Batch."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-azure-batch"
    pypi = (
        "snakemake_executor_plugin_azure_batch/snakemake_executor_plugin_azure_batch-0.1.3.tar.gz"
    )

    license("MIT")

    version("0.3.0", sha256="cafaa283ccabf9cb857c695eadf1dd8d47e9908a6497637b4bfa8e6c857a240c")
    version("0.2.1", sha256="9f828b2c0fa1b62b7160b8790894d325ffda58adec029118a39ad8f677b9a89a")
    version("0.2.0", sha256="5bfc6c63588595d9f815ab730b866940452999a677e2a5b7f474ede50125bff9")
    version("0.1.3", sha256="7883ecdc3983eb73ea0e1ae10010eeff1626510c7e99176203ee2050031f86e3")

    depends_on("py-snakemake-interface-common@1.17.2:1", type=("build", "run"), when="@0.2:")
    depends_on("py-snakemake-interface-common@1.15:1", type=("build", "run"))
    depends_on(
        "py-snakemake-interface-executor-plugins@9.2.0:9", type=("build", "run"), when="@0.2:"
    )
    depends_on(
        "py-snakemake-interface-executor-plugins@8.1.1:8", type=("build", "run"), when="@:0.1"
    )

    depends_on("py-azure-storage-blob@12.20:12", type=("build", "run"), when="@0.2:")
    depends_on("py-azure-storage-blob@12.17:12", type=("build", "run"))
    depends_on("py-azure-batch@14.2:14", type=("build", "run"), when="@0.2:")
    depends_on("py-azure-batch@14", type=("build", "run"))
    depends_on("py-azure-mgmt-batch@17", type=("build", "run"))
    depends_on("py-azure-identity@1.17.1:1", type=("build", "run"), when="@0.2:")
    depends_on("py-azure-identity@1.14:1", type=("build", "run"))
    depends_on("py-msrest@0.7.1:0.7", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
