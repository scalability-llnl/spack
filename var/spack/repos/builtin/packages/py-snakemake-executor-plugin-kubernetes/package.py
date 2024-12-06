# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginKubernetes(PythonPackage):
    """A Snakemake executor plugin for submission of jobs to Kubernetes."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-kubernetes"
    pypi = "snakemake_executor_plugin_kubernetes/snakemake_executor_plugin_kubernetes-0.1.4.tar.gz"

    license("MIT")

    version("0.1.4", sha256="c3aeac87939ec5d038efdc3ba7dbbef5eeb3171c1b718b8af850b6287b9c54ff")

    depends_on("py-kubernetes@27.2:27", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14.1:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@8.0.2:8", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
