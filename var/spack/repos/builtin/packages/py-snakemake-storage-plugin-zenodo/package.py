# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginZenodo(PythonPackage):
    """A Snakemake storage plugin for reading from and writing to zenodo.org."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-zenodo"
    pypi = "snakemake_storage_plugin_zenodo/snakemake_storage_plugin_zenodo-0.1.2.tar.gz"

    license("MIT")

    version("0.1.2", sha256="3675e76ae5dc930664bbcc1132a957c6490199c366e4e1e607d1491a7a46cf3d")

    depends_on("py-requests@2.31:2", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14.4:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
