# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginS3(PythonPackage):
    """A Snakemake storage plugin for S3 API storage (AWS S3, MinIO, etc.)."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-s3"
    pypi = "snakemake_storage_plugin_s3/snakemake_storage_plugin_s3-0.2.9.tar.gz"

    license("MIT")

    version("0.2.12", sha256="339bd425e18baabfb1404ab91dfe56a26499bf728fa3359fb4e0b17b287786a8")
    version("0.2.11", sha256="edbac21ca22d2e674eaadf05f21c611891df37366d4fbd6a712d79172d788895")
    version("0.2.10", sha256="a4554d170b5621751aba20ee08e6357090471a0a68b173525b118580c287a12e")

    depends_on("py-boto3@1.34.63:1", type=("build", "run"), when="@0.2.12:")
    depends_on("py-boto3@1.33:1", type=("build", "run"))
    depends_on("py-botocore@1.34.63:1", type=("build", "run"), when="@0.2.12:")
    depends_on("py-botocore@1.33:1", type=("build", "run"))
    depends_on("py-urllib3@2:2.1", type=("build", "run"), when="@:0.2.11")

    depends_on("py-snakemake-interface-common@1.14:1", type=("build", "run"))
    depends_on(
        "py-snakemake-interface-storage-plugins@3.2.4:3", type=("build", "run"), when="@0.2.12:"
    )
    depends_on(
        "py-snakemake-interface-storage-plugins@3.2.2:3", type=("build", "run"), when="@0.2.11:"
    )
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
