# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gluegen(Package):
    """GlueGen is a tool which automatically generates the Java and JNI code
    necessary to call C libraries."""

    homepage = "https://jogamp.org/gluegen/www/"
    git = "https://github.com/WadeWalker/gluegen.git"

    license("Apache-2.0")

    version("java-11-fixes", branch="java-11-fixes", submodules=True)

    depends_on("c", type="build")  # generated

    # ant optional jar file to execute antlr tasks
    resource(
        name="ant-optional",
        sha256="89ea82846b9ff4f4a5d51c7b5504e30462c64ddb990b014af5ded93b7d5e2b82",
        url="https://repo1.maven.org/maven2/ant/optional/1.5.4/optional-1.5.4.jar",
        placement="ant-optional",
        expand=False,
    )

    # source file of jogadm version cpptask to support Fujitsu compiler
    resource(name="cpptasks", git="http://jogamp.org/cgit/ant-cpptasks.git", when="%fj")

    depends_on("ant", type="build")
    depends_on("java@11", type=("build", "run"))

    # Change java library directory for java11
    patch("javalib.aarch64.patch", when="target=aarch64:")

    # patch for build with Fujitsu Compiler
    patch("cpptasks.fj.patch", working_dir="ant-cpptasks", when="%fj")

    compiler_mapping = {"gcc": "gcc", "clang": "clang", "fj": "fcc"}

    def install(self, spec, prefix):
        ant = spec["ant"].command
        cname = spec.compiler.name
        compiler = self.compiler_mapping.get(cname, "gcc")
        antarg = ["-Dgcc.compat.compiler={0}".format(compiler)]

        if self.spec.satisfies("%fj"):
            with working_dir("ant-cpptasks"):
                ant()
            copy(
                join_path("ant-cpptasks", "target", "lib", "cpptasks.jar"),
                join_path("make", "lib"),
            )

        with working_dir("make"):
            ant(*antarg)

        install_tree("build", prefix.build)
        install(join_path("ant-optional", "optional-1.5.4.jar"), prefix.build)
        install_tree("make", prefix.make)
        filter_file("..", prefix, join_path(prefix.make, "build.xml"), string=True)

    def setup_build_environment(self, env):
        env.prepend_path(
            "CLASSPATH", join_path(self.stage.source_path, "ant-optional", "optional-1.5.4.jar")
        )

    def setup_run_environment(self, env):
        class_paths = find(prefix.build, "*.jar")
        classpath = os.pathsep.join(class_paths)
        env.prepend_path("CLASSPATH", classpath)

    def setup_dependent_build_environment(self, env, dependent_spec):
        class_paths = find(prefix.build, "*.jar")
        classpath = os.pathsep.join(class_paths)
        env.prepend_path("CLASSPATH", classpath)
