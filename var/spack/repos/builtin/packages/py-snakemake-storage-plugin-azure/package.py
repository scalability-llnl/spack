# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginAzure(PythonPackage):
    """A Snakemake storage plugin to read and write from Azure Blob Storage."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-azure"
    pypi = "snakemake_storage_plugin_azure/snakemake_storage_plugin_azure-0.1.4.tar.gz"

    license("MIT")

    version("0.4.2", sha256="f1b0395e466fa2f6a20247a23c240b418240dbd6eaf7a55af3b34714594891f0")
    version("0.4.1", sha256="5200670ee317a572aa8fe843847a3b9810da1584543b84f69b804b54802db11b")
    version("0.4.0", sha256="7b3fd1479d3a2f3447891dbd27b84aeb7380f526b68147d7d8f7aceda14bda62")
    version("0.3.0", sha256="95f58b2f355707a37fcf739a0e9172388acef8a1800242f2e0724154521a20e0")
    version("0.2.2", sha256="df1f5740005dcdbe765f3f6c1b52b657dacaa5177a7a6e981a00aa5f5f2b0be7")
    version("0.2.1", sha256="0fb2ccf234a6aa7d4ec1e17b2bb2ab9bf19b0bd00f49f587722504ba01ea7423")
    version("0.2.0", sha256="6eea1bc5ff7ab7f5261981eca929a5576dfb76382f597d86ea4863a3e2bac7e7")
    version("0.1.6", sha256="549e54daf878be652ac5a301b1aa2b4d63d48e21a3a1abe33c4c7b4da79cf8d6")
    version("0.1.5", sha256="c200d5ffc1d593083028014becba83ace43749a666f394e567435b7299566568")
    version("0.1.4", sha256="dcfcf285c9f1b1aa89db359afbf02b28d9e57a97ddac66747d3e46832e7ddbff")

    depends_on("py-azure-storage-blob@12.20:12", type=("build", "run"), when="@0.1.6:")
    depends_on("py-azure-storage-blob@12.19:12", type=("build", "run"))
    depends_on("py-azure-core@1.30.2:1", type=("build", "run"), when="@0.1.6:")
    depends_on("py-azure-core@1.29.5:1", type=("build", "run"))
    depends_on("py-azure-identity@1.17.1:1", type=("build", "run"), when="@0.1.6:")
    depends_on("py-azure-identity@1.15:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.17.2:1", type=("build", "run"), when="@0.1.6:")
    depends_on("py-snakemake-interface-common@1.15:1", type=("build", "run"))
    depends_on(
        "py-snakemake-interface-storage-plugins@3.2.3:3", type=("build", "run"), when="@0.1.6:"
    )
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
