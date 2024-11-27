# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginSlurmJobstep(PythonPackage):
    """A Snakemake executor plugin for running srun jobs inside of SLURM jobs
    (meant for internal use by snakemake-executor-plugin-slurm)."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-slurm-jobstep"
    pypi = (
        "snakemake_executor_plugin_slurm_jobstep/"
        "snakemake_executor_plugin_slurm_jobstep-0.2.1.tar.gz"
    )
    maintainers("w8jcik")

    license("MIT")

    version("0.2.1", sha256="58894d52b5998a34fa6f60ec511ff0bfde4a9ec96714bcaa3cd2f46cf8a33859")
    version("0.1.11", sha256="cafdac937796ab0dfc0354c42380167a44a1db00c4edc98ab736a6ace2201a94")
    version("0.1.10", sha256="321b6bdf7883a8fb40ff4aeeb88633502e4db8394e40b6628db41a430c2eae2b")

    depends_on("py-snakemake-interface-common@1.13:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@9", type=("build", "run"), when="@0.1.11:")
    depends_on(
        "py-snakemake-interface-executor-plugins@8.2:8", type=("build", "run"), when="@:0.1.10"
    )

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
