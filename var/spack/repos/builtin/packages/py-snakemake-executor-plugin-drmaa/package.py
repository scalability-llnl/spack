# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginDrmaa(PythonPackage):
    """A snakemake executor plugin for submission of jobs via DRMAA."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-drmaa"
    pypi = "snakemake_executor_plugin_drmaa/snakemake_executor_plugin_drmaa-0.1.3.tar.gz"

    license("MIT")

    version("0.1.3", sha256="1250d0f307bf3db3aa3f26f85ea5ecc7ae00b2598ea1e1afceab7a457042fa12")

    depends_on("py-snakemake-interface-common@1.13:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@8.1:8", type=("build", "run"))
    depends_on("py-drmaa@0.7.9:0.7", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
