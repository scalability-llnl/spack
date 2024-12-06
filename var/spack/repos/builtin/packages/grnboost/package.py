# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grnboost(Package):
    """GRNBoost is a library built on top of Apache Spark that implements a
    scalable strategy for gene regulatory network (GRN) inference.

    See https://github.com/aertslab/GRNBoost/blob/master/docs/user_guide.md
    for the user guide. The location of xgboost4j-<version>.jar and
    GRNBoost.jar are set to $XGBOOST_JAR and $GRNBOOST_JAR. Path to
    xgboost4j-<version>.jar is also added to CLASSPATH."""

    homepage = "https://github.com/aertslab/GRNBoost"

    license("BSD-3-Clause")

    version(
        "2017-10-9",
        git="https://github.com/aertslab/GRNBoost.git",
        commit="26c836b3dcbb85852d3c6f4b8340e8655434da02",
    )

    depends_on("sbt", type="build")
    depends_on("java", type=("build", "run"))
    depends_on("xgboost", type="run")
    depends_on("spark+hadoop", type="run")

    def setup_run_environment(self, env):
        grnboost_jar = join_path(self.prefix, "target", "scala-2.11", "GRNBoost.jar")
        xgboost_version = self.spec["xgboost"].version.string
        xgboost_jar = join_path(
            self.spec["xgboost"].prefix, "xgboost4j-" + xgboost_version + ".jar"
        )
        env.set("GRNBOOST_JAR", grnboost_jar)
        env.set("JAVA_HOME", self.spec["java"].prefix)
        env.set("CLASSPATH", xgboost_jar)
        env.set("XGBOOST_JAR", xgboost_jar)

    def install(self, spec, prefix):
        sbt = which("sbt")
        sbt("assembly")
        install_tree("target", prefix.target)
