# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hudi(MavenPackage):
    """Apache Hudi stands for Hadoop Upserts Deletes and Incrementals.
    Hudi manages the storage of large analytical datasets on DFS."""

    homepage = "https://hudi.apache.org/"
    url = "https://github.com/apache/hudi/archive/refs/tags/release-0.5.3.tar.gz"

    license("Apache-2.0")

    version("0.5.3", sha256="8cbf52007fddd07eebd20c8962cd630b05a8ae4c597523fd63db837a45a0b227")

    depends_on("java@8", type=("build", "run"))
