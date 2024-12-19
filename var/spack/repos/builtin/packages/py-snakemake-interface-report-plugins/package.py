# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceReportPlugins(PythonPackage):
    """The interface for Snakemake report plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-report-plugins"
    pypi = "snakemake_interface_report_plugins/snakemake_interface_report_plugins-1.0.0.tar.gz"

    license("MIT")

    version("1.1.0", sha256="b1ee444b2fca51225cf8a102f8e56633791d01433cd00cf07a1d9713a12313a5")
    version("1.0.0", sha256="02311cdc4bebab2a1c28469b5e6d5c6ac6e9c66998ad4e4b3229f1472127490f")

    depends_on("py-snakemake-interface-common@1.16:1", type=("build", "run"))

    depends_on("python@:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
