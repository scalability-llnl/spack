# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mahout(MavenPackage):
    """The Apache Mahout project's goal is to build an environment for
    quickly creating scalable performant machine learning applications."""

    homepage = "https://mahout.apache.org/"
    url = "https://archive.apache.org/dist/mahout/0.13.0/apache-mahout-distribution-0.13.0-src.tar.gz"
    list_url = "https://archive.apache.org/dist/mahout"
    list_depth = 1

    license("Apache-2.0")

    version("0.13.0", sha256="bbe5a584fa83eb4ea3e0c146256e3e913c225426434759458d1423508da7c519")
    version("0.12.2", sha256="cac9a3fd4f11b2cb850b86d1bd23aec90e960cfae91850c49056c2eaae71afba")
    version("0.12.1", sha256="32e334115e4b2bfa21ba58e888fc47cdde2ca32c915d1694ed6761bda3b05dbb")
    version("0.12.0", sha256="65f340072131b1178b7bf4da115782254bdb20d6abd9789f10fc6dfe1ea7e7ad")

    depends_on("java@8:", type=("build", "run"))
    depends_on("maven@3.3.3:", type="build")
