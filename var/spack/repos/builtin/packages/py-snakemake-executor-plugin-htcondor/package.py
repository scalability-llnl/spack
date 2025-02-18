# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySnakemakeExecutorPluginHtcondor(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to a HTCondor cluster."""

    homepage = "https://github.com/jannisspeer/snakemake-executor-plugin-htcondor"
    pypi = "snakemake_executor_plugin_htcondor/snakemake_executor_plugin_htcondor-0.1.2.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.1.2", sha256="c5268807ecb6810d1852cbf7ccde0b54394e1a824eb64baa55538ccf55328f45")

    depends_on("htcondor@23.4.0:23", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.15:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@9", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
