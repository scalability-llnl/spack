# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceExecutorPlugins(PythonPackage):
    """This package provides a stable interface for interactions between Snakemake and its
    executor plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-executor-plugins"
    pypi = "snakemake_interface_executor_plugins/snakemake_interface_executor_plugins-9.2.0.tar.gz"
    maintainers("w8jcik")

    license("MIT")

    version("9.2.0", sha256="67feaf438a0b8b041ec5f1a1dd859f729036c70c07c9fdad895135f5b949e40a")
    version("8.2.0", sha256="4c74e3e1751bab6b266baf8688e854b8b4c5c5e10f5e34c581f42d69af4ff13b")

    depends_on("py-argparse-dataclass@2", type=("build", "run"))
    depends_on("py-throttler@1.2.2:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.12:1", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
