# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginAzure(PythonPackage):
    """A Snakemake storage plugin to read and write from Azure Blob Storage."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-azure"
    pypi = "snakemake_storage_plugin_azure/snakemake_storage_plugin_azure-0.1.4.tar.gz"

    license("MIT")

    version("0.1.4", sha256="dcfcf285c9f1b1aa89db359afbf02b28d9e57a97ddac66747d3e46832e7ddbff")

    depends_on("py-azure-storage-blob@12.19:12", type=("build", "run"))
    depends_on("py-azure-core@1.29.5:1", type=("build", "run"))
    depends_on("py-azure-identity@1.15:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.15:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
