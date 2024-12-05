# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Spark(Package):
    """Apache Spark is a fast and general engine
    for large-scale data processing.
    """

    homepage = "https://spark.apache.org"
    url = "https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0-bin-without-hadoop.tgz"

    maintainers("teaguesterling")

    variant("hadoop", default=False, description="Build with Hadoop")

    depends_on("java", type=("build", "run"))
    depends_on("hadoop", when="+hadoop", type=("build", "run"))

    license("Apache-2.0")

    version("3.5.1", sha256="5548c02625676fa97cb6b8072f131ed0b860a09d1e86be4e025d0cbfa869bc4a")
    version("3.4.3", sha256="85caa74671d46640a2ecccc5248ef673842b507b9843aeebccd6891721b6673f")
    version("3.3.4", sha256="793205ff45ce2cb4d91bb2c2724c14fb2a2a49754b93f36c60c4f47e100c2b10")
    version("3.2.4", sha256="9a824ad6d73797d602027d650f515d8b68269ffa52a64ff15cfedf10d85fe049")
    version("3.1.1", sha256="2d16f527016993e69a7c801233e661a170e3099ae2d9b950f7457729d63062f4")
    version("3.0.2", sha256="1a904f9bfa44a1218cb440c99800dd2ae729249a73c63b3bb10e431ed5b58406")
    version("3.0.1", sha256="ddda310ac09e3f2da9c33ad278b1665fbad2411d8da127d0de86b90019e962dc")
    version("2.4.7", sha256="f68f6a63814078ba3246dbf755f597b814a228122b239b07efb3909f017ddf8b")
    version("2.3.0", sha256="a7e29e78bd43aa6d137f0bb0afd54a3017865d471456c6d436ae79475bbeb161")
    version("2.1.0", sha256="3ca4ecb0eb9a00de5099cc2564ed957433a2d15d9d645a60470324621853c5ae")
    version("2.0.2", sha256="122ec1af0fcb23c0345f20f77d33cf378422ffe966efe4b9ef90e55cf7a46a3c")
    version("2.0.0", sha256="7c90bc4b7689df30f187e00845db8c7c9fb4045a0bcf2fa70a4954cc17d2c0d1")
    version("1.6.2", sha256="f6b43333ca80629bacbbbc2e460d21064f53f50880f3f0a3f68745fdf8b3137e")
    version("1.6.1", sha256="3d67678c5cb5eeba1cab125219fa2f9f17609368ea462e3993d2eae7c8f37207")
    version("1.6.0", sha256="9f62bc1d1f7668becd1fcedd5ded01ad907246df287d2525cfc562d88a3676da")

    def install(self, spec, prefix):
        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir("bin")
        install_dir("conf")
        install_dir("jars")
        install_dir("python")
        install_dir("R")
        install_dir("sbin")
        install_dir("yarn")

        # required for spark to recognize binary distribution
        install("RELEASE", prefix)

    @when("+hadoop")
    def setup_run_environment(self, env):
        hadoop = self.spec["hadoop"].command
        hadoop.add_default_env("JAVA_HOME", self.spec["java"].home)
        hadoop_classpath = hadoop("classpath", output=str)

        # Remove whitespaces, as they can compromise syntax in
        # module files
        hadoop_classpath = re.sub(r"[\s+]", "", hadoop_classpath)

        env.set("SPARK_DIST_CLASSPATH", hadoop_classpath)
