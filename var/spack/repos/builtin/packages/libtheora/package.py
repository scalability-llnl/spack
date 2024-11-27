# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import sys

from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.msbuild import MSBuildBuilder
from spack.package import *


class Libtheora(AutotoolsPackage, MSBuildPackage):
    """Theora Video Compression."""

    homepage = "https://www.theora.org"
    url = "https://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.xz"
    git = "https://gitlab.xiph.org/xiph/theora.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("stable", branch="theora-1.1")
    version("1.1.1", sha256="f36da409947aa2b3dcc6af0a8c2e3144bc19db2ed547d64e9171c59c66561c61")
    version("1.1.0", sha256="3d7b4fb1c115f1a530afd430eed2e8861fa57c8b179ec2d5a5d8f1cd0c7a4268")

    depends_on("c", type="build")  # generated

    variant("doc", default=False, description="Build documentation")

    depends_on("doxygen", when="+doc", type="build")
    depends_on("libogg")
    depends_on("libpng")
    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")

    with when("platform=windows"):
        variant(
            "static",
            default=True,
            description="Enable static build, if false shared library is built",
        )

    build_system(
        "msbuild", "autotools", default="autotools" if sys.platform != "win32" else "msbuild"
    )

    patch("fix_encoding.patch", when="@1.1:")
    patch(
        "https://gitlab.xiph.org/xiph/theora/-/commit/7288b539c52e99168488dc3a343845c9365617c8.diff",
        sha256="e01ef71a1c19783a0b323b90a625e5c360ddb7ee03d2b6c201f1519f1704ea11",
        when="@:1.1.1 ^libpng@1.6:",
    )
    # add -no-undefined
    patch(
        "https://gitlab.xiph.org/xiph/theora/-/commit/391ab0e99f2ad730231dbe5fc1154b990087f17d.diff",
        sha256="d9bb5a9573819a27b3a925b1b66c33b36d9bca11b05d8aef88566eb6c8700690",
        when="@:1.1.1",
    )
    # link theoraenc to theoradec
    patch(
        "https://gitlab.xiph.org/xiph/theora/-/commit/133b951b60fd845eabbc38bf7acd998bb9be75fc.diff",
        sha256="e01511aff0130a40c889868d3713a56458744f39d1bb5ad98c8058da50233aa7",
        when="@:1.1.1",
    )
    patch("libtheora-inc-external-ogg.patch", when="platform=windows")


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        args = []
        args += self.enable_or_disable("doc")
        args += ["LIBS=-lm"]
        return args


class MSBuildBuilder(MSBuildBuilder):
    def is_64bit(self):
        return "64" in str(self.pkg.spec.target.family)

    def setup_build_environment(self, env):
        spec = self.pkg.spec
        env.set("SPACK_OGG_PREFIX", spec["libogg"].prefix)
        # devenv is needed to convert ancient MSbuild project to modern
        # msbuild project so MSBuild versions older than 2010 can build this
        # project
        devenv_path = os.path.join(self.pkg.compiler.vs_root, "Common7", "IDE")
        env.prepend_path("PATH", devenv_path)

    @property
    def build_directory(self):
        win_dir = os.path.join(super().build_directory, "win32")
        vs_dir = "VS2008"
        return os.path.join(win_dir, vs_dir)

    @property
    def sln_file(self):
        if self.pkg.spec.satisfies("+static"):
            f = "libtheora_static.sln"
        else:
            f = "libtheora_dynamic.sln"
        return f

    def msbuild_args(self):
        return [self.define("Configuration", "Release"), self.sln_file]

    def build(self, pkg, spec, prefix):
        with working_dir(self.build_directory):
            devenv = Executable("devenv")
            devenv(self.sln_file, "/Upgrade")
        super().build(pkg, spec, prefix)

    def install(self, pkg, spec, prefix):
        mkdirp(prefix.lib)
        libs_to_install = glob.glob(
            os.path.join(self.build_directory, "**", "*.lib"), recursive=True
        )
        if self.pkg.spec.satisfies("~static"):
            libs_to_install.extend(
                glob.glob(os.path.join(self.build_directory, "**", "*.dll"), recursive=True)
            )
        for library in libs_to_install:
            install(library, prefix.lib)
        rename(
            os.path.join(prefix.lib, "libtheora_static.lib"),
            os.path.join(prefix.lib, "theora.lib"),
        )
        # The encoder and decoder libs are baked into the theora lib on Windows, so we spoof them
        # here so libtheora is detectable by CMake and pkg-config and linkable by
        # consuming projects
        with working_dir(prefix.lib):
            copy("theora.lib", "theoradec.lib")
            copy("theora.lib", "theoraenc.lib")
        with working_dir(pkg.stage.source_path):
            install_tree("include", prefix.include)
