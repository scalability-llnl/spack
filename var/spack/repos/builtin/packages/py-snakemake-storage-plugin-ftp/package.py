# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginFtp(PythonPackage):
    """A Snakemake plugin for handling input and output via FTP."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-ftp"
    pypi = "snakemake_storage_plugin_ftp/snakemake_storage_plugin_ftp-0.1.2.tar.gz"

    license("MIT")

    version("0.1.2", sha256="e3097e19dbe9ed4c8cf794e1d4594c3032ee7f7a9f7797dfb0d2556f0aafe07c")

    depends_on("py-ftputil@5.0.4:5", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.15.1:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
