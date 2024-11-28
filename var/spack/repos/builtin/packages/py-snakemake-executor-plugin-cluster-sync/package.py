# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginClusterSync(PythonPackage):
    """A Snakemake executor plugin for cluster jobs that are executed synchronously."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-cluster-sync"
    pypi = (
        "snakemake_executor_plugin_cluster_sync/"
        "snakemake_executor_plugin_cluster_sync-0.1.4.tar.gz"
    )

    license("MIT")

    version("0.1.4", sha256="6a6dcb2110d4c2ee74f9a48ea68e0fd7ddd2800672ebef00a01faa4affa835ad")
    version("0.1.3", sha256="c30fca6ccb98a3f7ca52ca8a95414c71360a3d4a835bd4a097a13445d6fce2ac")

    depends_on("py-snakemake-interface-common@1.14:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@9", type=("build", "run"), when="@0.1.4:")
    depends_on(
        "py-snakemake-interface-executor-plugins@8.1:8", type=("build", "run"), when="@:0.1.3"
    )

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
