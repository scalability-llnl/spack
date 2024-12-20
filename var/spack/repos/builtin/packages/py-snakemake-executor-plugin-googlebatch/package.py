# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginGooglebatch(PythonPackage):
    """A Snakemake executor plugin."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-googlebatch"
    pypi = (
        "snakemake_executor_plugin_googlebatch/snakemake_executor_plugin_googlebatch-0.3.0.tar.gz"
    )

    license("MIT")

    version("0.5.0", sha256="242ddb2348db1837a0676e991b257e0924791d3dab20aa8f89d63c548adfd1cd")
    version("0.4.0", sha256="ad1ebf74d6558bc5ea9d1849570fb3c5991413265c771d944e99aeb8c49217d2")
    version("0.3.3", sha256="fbc3f3dad6fca51f9d65cd66a6a1272b056213ed3ab03759523f27590c58bcd8")
    version("0.3.2", sha256="9f861f0067d96e825796c0a3aa829581a22036bfeb2c6d481c5c42daeaf7fcbf")
    version("0.3.1", sha256="292c024534e98aecf6a5a2be8a24db104d8038831b6a55fe50c87c1e4fdb28af")
    version("0.3.0", sha256="b143fcaeffceec682bc0f7e3f13eece3596a5d6faaf41fab94977f4a93948c16")

    depends_on("py-google-cloud-batch@0.17.1:0.17", type=("build", "run"))
    depends_on("py-requests@2.31:2", type=("build", "run"))
    depends_on("py-google-api-core@2.12:2", type=("build", "run"))
    depends_on("py-google-cloud-storage@2.12:2", type=("build", "run"))
    depends_on("py-jinja2@3.1.2:3", type=("build", "run"))
    depends_on("py-google-cloud-logging@3.8:3", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@9", type=("build", "run"), when="@0.3.1:")
    depends_on(
        "py-snakemake-interface-executor-plugins@8.1.1:8", type=("build", "run"), when="@:0.3.0"
    )

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
