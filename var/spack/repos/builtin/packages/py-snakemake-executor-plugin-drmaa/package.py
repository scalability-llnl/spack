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

    version("0.1.5", sha256="24fe16fc1f1e7ef75bc213cdb960b674bb130ec918a9f6106511a667ffc661b2")
    version("0.1.4", sha256="93ddefc3fcb5ee2241e4622d04fd1ffcfc58776ff9e723e958a0da2cc2c5fcb7")
    version("0.1.3", sha256="1250d0f307bf3db3aa3f26f85ea5ecc7ae00b2598ea1e1afceab7a457042fa12")

    depends_on("py-snakemake-interface-common@1.13:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@9", type=("build", "run"), when="@0.1.4:")
    depends_on(
        "py-snakemake-interface-executor-plugins@8.1:8", type=("build", "run"), when="@:0.1.3"
    )
    depends_on("py-drmaa@0.7.9:0.7", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
