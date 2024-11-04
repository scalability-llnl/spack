# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginSlurm(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to a SLURM cluster."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-slurm"
    pypi = "snakemake_executor_plugin_slurm/snakemake_executor_plugin_slurm-0.10.0.tar.gz"
    maintainers("w8jcik")

    license("MIT")

    version("0.10.0", sha256="d970bd08e00f1664adbd3c421c956b2ce926359ff10a4d7650c444c1179bec3f")
    version("0.3.2", sha256="3912f2895eab1270d7a42959a2e221ce53428dfffb847e03ec6bc4eead88e30b")

    depends_on("py-throttler@1.2.2:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.13:1", type=("build", "run"))

    depends_on(
        "py-snakemake-interface-executor-plugins@9.1.1:9", type=("build", "run"), when="@0.4.4:"
    )
    depends_on(
        "py-snakemake-interface-executor-plugins@9", type=("build", "run"), when="@0.4.2:0.4.3"
    )
    depends_on(
        "py-snakemake-interface-executor-plugins@8.2:8", type=("build", "run"), when="@:0.4.1"
    )

    depends_on(
        "py-snakemake-executor-plugin-slurm-jobstep@0.2", type=("build", "run"), when="@0.4.4:"
    )
    depends_on(
        "py-snakemake-executor-plugin-slurm-jobstep@0.1.10:0.1",
        type=("build", "run"),
        when="@:0.4.3",
    )

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
