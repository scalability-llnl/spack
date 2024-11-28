# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Telegraf(MakefilePackage):
    """Telegraf is an agent for collecting, processing, aggregating,
    and writing metrics."""

    homepage = "https://github.com/influxdata/telegraf"
    url = "https://github.com/influxdata/telegraf/archive/refs/tags/v1.19.3.tar.gz"

    license("MIT")

    version("1.30.2", sha256="3514d870fe1899f20c5d1f1545233413cbe11061b23a0cafbd44b861a9295dc6")
    version("1.20.3", sha256="cf8fd4d38970648281101e8a71b1a48c5765c8aaa9d67619c00272c9192e9057")
    version("1.19.3", sha256="d2fb8a3519a5690c801e1221e22c3693ed95204f70f6c57eb13267ca1964c659")

    depends_on("go", type="build")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("telegraf", prefix.bin)
        install_tree("docs", prefix.docs)
