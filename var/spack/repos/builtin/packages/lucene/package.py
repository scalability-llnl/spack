# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lucene(Package):
    """
    Apache Lucene is a high-performance, full featured text search engine
    library written in Java.
    """

    homepage = "https://lucene.apache.org/"
    url = "https://archive.apache.org/dist/lucene/java/8.3.1/lucene-8.3.1.tgz"
    list_url = "https://archive.apache.org/dist/lucene/java/"
    list_depth = 1

    license("Apache-2.0", checked_by="wdconinc")

    version("10.0.0", sha256="b40c29039c363a9479947acfbc41efb381af7868233446412d625a197436a243")
    version(
        "9.12.0",
        sha256="8d7c698e7bdee7580950c4323f091b996afb1b14c91d6d6e4e150ccff883c6c5",
        preferred=True,
    )
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2024-45772
        version(
            "9.10.0", sha256="c57b75ee0ea12b54337967b7854ebd12af3d7bad27245c1dc12a167ce2b1f8a7"
        )
        version("9.5.0", sha256="547277a2b6ce283422eccd14e9ee7ffb28b1af3975936959716c9b4d85843555")
        version("8.3.1", sha256="acd61ad458d16f3c98b9dd4653c6a34dd666a965842e461f7cdf8947fa041e1a")
        version("8.3.0", sha256="67c4f8081f24ff9f4eb4f2b999ac19f7a639b416e5b6f1c1c74e0524a481fc7e")
        version("8.2.0", sha256="505cad34698b217fd6ceee581a8215223a47df5af820c94ca70a6bdbba9d5d7c")
        version("8.1.1", sha256="d62b0acdf2b1ed7a25ccdb593ad8584caeaa20cc9870e22790d3ec7fa6240a8c")

    # build.gradle minJavaVersion or versions.toml minJava
    depends_on("java@8:", type="run")
    depends_on("java@11:", type="run", when="@9:")
    depends_on("java@21:", type="run", when="@10:")

    def install(self, spec, prefix):
        install_tree(".", prefix)
