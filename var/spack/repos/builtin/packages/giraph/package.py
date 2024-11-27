# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Giraph(MavenPackage):
    """Apache Giraph is an iterative graph processing system built
    for high scalability."""

    homepage = "https://giraph.apache.org/"
    url = "https://downloads.apache.org/giraph/giraph-1.0.0/giraph-dist-1.0.0-src.tar.gz"
    list_url = "https://downloads.apache.org/giraph/"
    list_depth = 1

    license("Apache-2.0")

    version("1.2.0", sha256="6206f4ad220ea42aa0c4abecce343e36026cf9c6e0a2853f1eb08543da452ad1")
    version("1.1.0", sha256="181d94b8198c0f312d4611e24b0056b5181c8358a7ec89b0393661736cd19a4c")

    depends_on("java@7:", type=("build", "run"))
    depends_on("maven@3.0.0:", type="build")

    def install(self, spec, prefix):
        giraph_path = join_path(
            self.stage.source_path,
            "giraph-dist",
            "target",
            "giraph-{0}-for-hadoop-1.2.1-bin".format(spec.version),
            "giraph-{0}-for-hadoop-1.2.1".format(spec.version),
        )
        with working_dir(giraph_path):
            install_tree(".", prefix)
