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

    version("0.1.3", sha256="f0315596120160656b8c8afec66e3b31b4a2889b9d0cead2102f9d924ec0b326")

    depends_on("py-google-cloud-storage@2.12:2", type=("build", "run"))
    depends_on("py-google-crc32c@1.1.2:1", type=("build", "run"))

    # This is not in the package definition, but I am pretty sure that it is needed
    # https://github.com/snakemake/snakemake-storage-plugin-gcs/issues/19
    depends_on("py-snakemake-interface-common@1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
