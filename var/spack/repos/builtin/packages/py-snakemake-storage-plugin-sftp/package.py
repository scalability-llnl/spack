# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginSftp(PythonPackage):
    """A Snakemake storage plugin that handles files on an SFTP server."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-sftp"
    pypi = "snakemake_storage_plugin_sftp/snakemake_storage_plugin_sftp-0.1.2.tar.gz"

    license("MIT")

    version("0.1.2", sha256="1b5f99a6baf334d74e209d6ec8a59e495e56098cf6e9a19954e472ba1501525c")

    depends_on("py-pysftp@0.2.9:0.2", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14.3:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
