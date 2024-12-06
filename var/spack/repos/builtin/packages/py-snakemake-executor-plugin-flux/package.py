# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginFlux(PythonPackage):
    """A Snakemake executor plugin for the Flux scheduler."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-flux"
    pypi = "snakemake_executor_plugin_flux/snakemake_executor_plugin_flux-0.1.0.tar.gz"

    license("MIT")

    version("0.1.0", sha256="92b1944dcf9ea163519a8879d4d638df2b3d0cd83ea6e8397d26046897811214")

    depends_on("py-snakemake-interface-common@1.14:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@8.1.1:8", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
