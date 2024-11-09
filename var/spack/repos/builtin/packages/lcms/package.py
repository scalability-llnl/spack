# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib

from spack.package import *


class Lcms(AutotoolsPackage, MSBuildPackage):
    """Little cms is a color management library. Implements fast
    transforms between ICC profiles. It is focused on speed, and is
    portable across several platforms (MIT license)."""

    homepage = "https://www.littlecms.com"
    url = "https://downloads.sourceforge.net/project/lcms/lcms/2.9/lcms2-2.9.tar.gz"

    license("MIT")

    version("2.16", sha256="d873d34ad8b9b4cea010631f1a6228d2087475e4dc5e763eb81acc23d9d45a51")
    version("2.15", sha256="b20cbcbd0f503433be2a4e81462106fa61050a35074dc24a4e356792d971ab39")
    version("2.14", sha256="28474ea6f6591c4d4cee972123587001a4e6e353412a41b3e9e82219818d5740")
    version("2.13.1", sha256="d473e796e7b27c5af01bd6d1552d42b45b43457e7182ce9903f38bb748203b88")
    version("2.9", sha256="48c6fdf98396fa245ed86e622028caf49b96fa22f3e5734f853f806fbc8e7d20")
    version("2.8", sha256="66d02b229d2ea9474e62c2b6cd6720fde946155cd1d0d2bffdab829790a0fb22")
    version("2.6", sha256="5172528839647c54c3da211837225e221be93e4733f5b5e9f57668f7107e14b1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/lcms/lcms/{0}/lcms2-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    depends_on("jpeg")
    depends_on("libtiff")
    depends_on("zlib-api")

    build_system("autotools", "msbuild")

    @property
    def libs(self):
        return find_libraries("liblcms2", root=self.prefix, recursive=True)


class MSBuildBuilder(spack.build_systems.msbuild.MSBuildBuilder):
    @property
    def build_directory(self):
        return (
            pathlib.Path(self.pkg.stage.source_path)
            / "Projects"
            / f"VC{self.pkg.compiler.visual_studio_version}"
        )

    def setup_build_environment(self, env):
        env.prepend_path(
            "INCLUDE",
            ";".join([dep.prefix.include for dep in self.spec.dependencies(deptype="link")]),
        )

    def msbuild_args(self):
        return ["lcms2.sln"]
