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

    version("0.3.0", sha256="b143fcaeffceec682bc0f7e3f13eece3596a5d6faaf41fab94977f4a93948c16")

    depends_on("py-google-cloud-batch@0.17.1:0.17", type=("build", "run"))
    depends_on("py-requests@2.31:2", type=("build", "run"))
    depends_on("py-google-api-core@2.12:2", type=("build", "run"))
    depends_on("py-google-cloud-storage@2.12:2", type=("build", "run"))
    depends_on("py-jinja2@3.1.2:3", type=("build", "run"))
    depends_on("py-google-cloud-logging@3.8:3", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@8.1.1:8", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
