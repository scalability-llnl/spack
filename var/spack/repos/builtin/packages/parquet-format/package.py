# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ParquetFormat(MavenPackage):
    """ParquetFormat is a columnar storage format that supports nested data."""

    homepage = "https://github.com/apache/parquet-format/"
    url = "https://github.com/apache/parquet-format/archive/apache-parquet-format-2.8.0.tar.gz"

    license("Apache-2.0")

    version("2.8.0", sha256="345c044cea73997162e0c38ae830509ee424faf49c90974e4f244079a3df01b0")
    version("2.7.0", sha256="e821ffc67f61b49afce017ce2d1d402b4df352ca49dbeae167b06c4d3264b6ba")

    depends_on("thrift@0.12.0", when="@2.7.0:")
    depends_on("java@8", type=("build", "run"))
