# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Jogl(Package):
    """JOGL provides full access to the APIs in the OpenGL specification
    as well as nearly all vendor extensions."""

    homepage = "https://jogamp.org/jogl/www/"
    git = "https://github.com/WadeWalker/jogl.git"

    license("Apache-2.0")

    version("java-11-fixes", branch="java-11-fixes", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("ant", type="build")
    depends_on("java", type=("build", "run"))
    depends_on("gluegen", type=("build", "run"))
    depends_on("gl", type="link")
    depends_on("glu", type="link")
    depends_on("libxcursor", type="link")

    # Xfree86 Video mode extentions is deprecated
    patch("noxf86vm.patch")

    phases = ["edit", "build", "install"]

    def edit(self, spec, prefix):
        common = join_path("make", "build-common.xml")
        filter_file("../../gluegen", spec["gluegen"].prefix, common)
        for target in ["nativewindow", "jogl", "newt"]:
            conf = join_path("make", "build-{0}.xml".format(target))
            filter_file(r'syslibset dir="\${env.TARGET_PLATFORM_ROOT}[^"]*"', "syslibset", conf)
            filter_file("/usr/include", spec["libxcursor"].prefix.include, conf)

    compiler_mapping = {"gcc": "gcc", "clang": "clang", "fj": "fcc"}

    def build(self, spec, prefix):
        cname = spec.compiler.name
        compiler = self.compiler_mapping.get(cname, "gcc")
        ant = spec["ant"].command
        antarg = ["-Dcommon.gluegen.build.done=true", "-Dgcc.compat.compiler={0}".format(compiler)]
        with working_dir("make"):
            ant(*antarg)

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        with working_dir(join_path("build", "jar")):
            install("*.jar", prefix.lib)
        with working_dir(join_path("build", "lib")):
            install("*.so", prefix.lib)

    def setup_build_environment(self, env):
        env.unset("CLASSPATH")

    def setup_run_environment(self, env):
        class_paths = find(prefix.lib, "*.jar")
        classpath = os.pathsep.join(class_paths)
        env.prepend_path("CLASSPATH", classpath)

    def setup_dependent_build_environment(self, env, dependent_spec):
        class_paths = find(prefix.lib, "*.jar")
        classpath = os.pathsep.join(class_paths)
        env.prepend_path("CLASSPATH", classpath)
