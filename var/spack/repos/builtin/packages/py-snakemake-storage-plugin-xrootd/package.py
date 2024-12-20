# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySnakemakeStoragePluginXrootd(PythonPackage):
    """A Snakemake storage plugin to read and write from XRootD Storage."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-xrootd"
    pypi = "snakemake_storage_plugin_xrootd/snakemake_storage_plugin_xrootd-0.1.4.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.1.4", sha256="61a48b2567fa7f35a29f00f0a74d1efd069a16c0ef7c9f7f440a46088d2c6dbc")

    depends_on("xrootd@5.6.4:5 +python", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.15:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3.3.0:3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
