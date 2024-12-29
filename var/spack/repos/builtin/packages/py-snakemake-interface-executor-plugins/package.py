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

    version("9.3.2", sha256="19c50dc82989ff25d10386cfb3c99da9d2dc980d95ecd30bbb431374dcd390b3")
    version("9.3.1", sha256="98e1b7a6c5e0997ac391812ab66a79822c38ac98ea9322f2fd8d6a1294e219a0")
    version("9.3.0", sha256="11e70cf3d821d9f071b18b8a8147bc4dbad37f3ee68647f72aa3c80c4ab5c8dc")
    version("9.2.0", sha256="67feaf438a0b8b041ec5f1a1dd859f729036c70c07c9fdad895135f5b949e40a")
    version("8.2.0", sha256="4c74e3e1751bab6b266baf8688e854b8b4c5c5e10f5e34c581f42d69af4ff13b")

    depends_on("py-argparse-dataclass@2", type=("build", "run"))
    depends_on("py-throttler@1.2.2:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.17.4:1", type=("build", "run"), when="@9.3:")
    depends_on("py-snakemake-interface-common@1.12:1", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
