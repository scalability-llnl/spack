# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginFs(PythonPackage):
    """A Snakemake storage plugin that reads and writes from a locally mounted filesystem
    using rsync."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-fs"
    pypi = "snakemake_storage_plugin_fs/snakemake_storage_plugin_fs-0.1.5.tar.gz"

    license("MIT")

    version("0.2.0", sha256="cad1859036cbf429ea6fdb97f242567ec54a36d0b6ff900ce0d3ecfb6a824ae7")

    depends_on("py-sysrsync@1.1.1:1", type=("build", "run"))
    depends_on("py-reretry@0.11.8:0.11", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.17:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3.1:3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
