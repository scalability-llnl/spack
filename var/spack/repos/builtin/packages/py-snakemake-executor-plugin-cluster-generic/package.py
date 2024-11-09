# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginClusterGeneric(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to a cluster."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-cluster-generic"
    pypi = (
        "snakemake_executor_plugin_cluster_generic/"
        "snakemake_executor_plugin_cluster_generic-1.0.9.tar.gz"
    )

    license("MIT")

    version("1.0.9", sha256="ad0dc2d8bde7d4f336364bebe11a3b2209653c481ce8fbb0ae8bec81016a9a14")
    version("1.0.7", sha256="093808e63cc48294a9d1eb0b620cdff8cc970806294a2f6ba127a49f8a81d473")

    depends_on("py-snakemake-interface-common@1.13:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@9", type=("build", "run"), when="@1.0.9:")
    depends_on(
        "py-snakemake-interface-executor-plugins@8.1:8", type=("build", "run"), when="@:1.0.8"
    )

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
