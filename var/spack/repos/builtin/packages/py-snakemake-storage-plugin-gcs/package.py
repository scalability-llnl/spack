# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginGcs(PythonPackage):
    """A Snakemake storage plugin for Google Cloud Storage."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-gcs"
    pypi = "snakemake_storage_plugin_gcs/snakemake_storage_plugin_gcs-0.1.3.tar.gz"

    license("MIT")

    version("1.1.2", sha256="417f0dfdd6c28b3ceed609c2d29d18a135039e28433d45058eb8cb7b5a7e061a")
    version("1.1.1", sha256="ac6fc6aaf63ec6ae7453e1cb080e07da346ad4497bd2a87947c352f0fb311d31")
    version("1.1.0", sha256="841ef25be8fa7c6f13b45fd2428c71281e05ef28ce8235f7775e19820fa4564c")
    version("1.0.0", sha256="a5ca15813a74ae18d41cc5dbde0792e2ec5bfc32e8615d458b41dded1b430e14")
    version("0.1.4", sha256="f8c2ebbc2b44ff5a87f7507b26bd1176de98ae80e93339b2ae65f722d17dbc24")
    version("0.1.3", sha256="f0315596120160656b8c8afec66e3b31b4a2889b9d0cead2102f9d924ec0b326")

    depends_on("py-google-cloud-storage@2.12:2", type=("build", "run"))
    depends_on("py-google-crc32c@1.1.2:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14.2:1", type=("build", "run"), when="@0.1.4:")
    depends_on("py-snakemake-interface-common@1", type=("build", "run"))
    depends_on(
        "py-snakemake-interface-storage-plugins@3.3:3", type=("build", "run"), when="@1.1.1:"
    )
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
