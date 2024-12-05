# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginTes(PythonPackage):
    """A Snakemake executor plugin for submitting jobs via GA4GH TES."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-tes"
    pypi = "snakemake_executor_plugin_tes/snakemake_executor_plugin_tes-0.1.2.tar.gz"

    license("MIT")

    version("0.1.2", sha256="bec01801ae3f158cfe7ca406a513455bcffa36fa7f83e35b2c7cb93bec9b00e9")

    depends_on("py-py-tes@0.4.2:0.4", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@8.1.1:8", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
