# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Justbuild(Package):
    "just, a generic build tool"

    git = "https://github.com/just-buildsystem/justbuild.git"

    homepage = "https://github.com/just-buildsystem/justbuild"

    tags = ["build-tools"]

    executables = ["^just$"]

    maintainers("asartori86")

    license("Apache-2.0")

    version("master", branch="master")
    version("1.3.2", tag="v1.3.2", commit="27a56845398b07471f8185648a79a63f97851659")
    version("1.3.1", tag="v1.3.1", commit="b248838ed0f01bc5824caee3a555e7fd22d5ad10")
    version("1.3.0", tag="v1.3.0", commit="a7be2417f358049e6a0e28e01bc4020d8de2fdc5")
    version("1.2.5", tag="v1.2.5", commit="0f7447e3f50e68ecfe00b2db06fb5f154842ac5a")
    version("1.2.4", tag="v1.2.4", commit="215e6afab93d28aeea54cb2c657afda0e5453307")
    version("1.2.3", tag="v1.2.3", commit="45e9c1c85399f00372ad8b72894979a0002d8f95")
    version("1.2.2", tag="v1.2.2", commit="e1ee04684c34ae30ac3c91b6753e99a81a9dc51c")
    version("1.2.1", tag="v1.2.1", commit="959cd90083d0c783389cd09e187c98322c16469f")
    version("1.1.4", tag="v1.1.4", commit="32e96afd159f2158ca129fd00bf02c273d8e1e48")
    version("1.1.3", tag="v1.1.3", commit="3aed5d450aec38be18edec822ac2efac6d49a938")
    version("1.1.2", tag="v1.1.2", commit="67b486e2ce6ab657a98b2212a9b6f68935d07a29")
    version("1.0.0", tag="v1.0.0", commit="c29b671f798e82ba26b5f54ebc9e24c7dcfb8166")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3:", type=("build", "run"))
    depends_on("wget", type=("build", "run"))

    sanity_check_is_file = [join_path("bin", "just"), join_path("bin", "just-mr")]

    def setup_build_environment(self, env):
        ar = which("ar")
        if self.spec.version < Version("1.2.1"):
            family = ', "COMPILER_FAMILY":"unknown"'
        else:
            family = ', "TOOLCHAIN_CONFIG": {"FAMILY": "unknown"}'
        if self.spec.satisfies("%gcc@10:"):
            gcc = which("gcc")
            gpp = which("g++")
            env.set(
                "JUST_BUILD_CONF",
                "  {"
                + '  "CC":"{0}"'.format(gcc.path)
                + ', "CXX":"{0}"'.format(gpp.path)
                + ', "AR":"{0}"'.format(ar.path)
                + family
                + ', "ENV":{'
                + '    "PATH":"{0}"'.format(os.environ["PATH"])
                + "   }"
                + "}",
            )
        elif self.spec.satisfies("%clang@11:") or spec.satisfies("%apple-clang@11:"):
            clang = which("clang")
            clangpp = which("clang++")
            env.set(
                "JUST_BUILD_CONF",
                "  {"
                + '  "CC":"{0}"'.format(clang.path)
                + ', "CXX":"{0}"'.format(clangpp.path)
                + ', "AR":"{0}"'.format(ar.path)
                + ', "COMPILER_FAMILY":"unknown"'
                + ', "ENV":{'
                + '    "PATH":"{0}"'.format(os.environ["PATH"])
                + "   }"
                + "}",
            )
        else:
            raise InstallError("please use gcc >= 10 or clang >= 11")

    def install(self, spec, prefix):
        python = which("python3")
        python(os.path.join("bin", "bootstrap.py"), ".", prefix)
        mkdirp(prefix.bin)
        install(os.path.join(prefix, "out", "bin", "just"), prefix.bin)
        install(os.path.join("bin", "just-mr.py"), os.path.join(prefix.bin, "just-mr"))

    @classmethod
    def determine_version(cls, exe):
        import json

        try:
            s = os.popen(exe + " version").read()
            d = json.loads(s)
            return ".".join(map(str, d["version"])) + d["suffix"].replace("~", "-")
        except Exception:
            return None
