# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginSlurm(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to a SLURM cluster."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-slurm"
    pypi = "snakemake_executor_plugin_slurm/snakemake_executor_plugin_slurm-0.10.0.tar.gz"
    maintainers("w8jcik")

    license("MIT")

    version("0.11.2", sha256="fca29038d78387c237afb4ec2b04638e6128d2456940dd7b96ac4205f319d7f3")
    version("0.11.1", sha256="293a951dcf829400bf6197705d6c602faed95aaaae9ad0d661d23b0184074134")
    version("0.11.0", sha256="bce1df57900da71175c1c384dbc8f04d8bf8572717c0aaf95c32945a4c7a08d3")
    version("0.10.2", sha256="919beb114785545f3cc187988f9257a183f1a2c76593e8a8559b87962ebd2651")
    version("0.10.1", sha256="0d117e3b6fb523b873bd04b7e0117a0c83c9b38dfef1b0a79535c7a084e982ea")
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
