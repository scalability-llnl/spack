# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceStoragePlugins(PythonPackage):
    """This package provides a stable interface for interactions between Snakemake and its storage
    plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-storage-plugins"
    pypi = "snakemake_interface_storage_plugins/snakemake_interface_storage_plugins-3.3.0.tar.gz"
    maintainers("w8jcik")

    license("MIT")

    version("3.3.0", sha256="203d8f794dfb37d568ad01a6c375fa8beac36df8e488c0f9b9f75984769c362a")
    version("3.1.0", sha256="26e95be235ef2a9716b890ea96c3a9a2e62061c5d72fbb89c2fad2afada87304")

    depends_on("py-wrapt@1.15:1", type=("build", "run"))
    depends_on("py-reretry@0.11.8:0.11", type=("build", "run"))
    depends_on("py-throttler@1.2.2:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.12:1", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
