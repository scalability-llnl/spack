# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginHttp(PythonPackage):
    """Snakemake storage plugin for downloading input files from HTTP(s)."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-http"
    pypi = "snakemake_storage_plugin_http/snakemake_storage_plugin_http-0.2.3.tar.gz"

    license("MIT")

    version("0.2.3", sha256="e4944a7c134e98515d9473c867c4ce071e3b625a5a9002a00da6ac917bc0c0ad")

    depends_on("py-requests@2.31:2", type=("build", "run"))
    depends_on("py-requests-oauthlib@1.3.1:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
