# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.build_systems.makefile
from spack.package import *


class Alpgen(CMakePackage, MakefilePackage):
    """A collection of codes for the generation of multi-parton processes
    in hadronic collisions.
    """

    homepage = "http://mlm.home.cern.ch/mlm/alpgen/"
    url = "http://mlm.home.cern.ch/mlm/alpgen/V2.1/v214.tgz"

    tags = ["hep"]

    version("2.1.4", sha256="2f43f7f526793fe5f81a3a3e1adeffe21b653a7f5851efc599ed69ea13985c5e")

    build_system("makefile", "cmake", default="makefile")

    variant(
        "recipe",
        values=(
            conditional("cms", when="build_system=makefile"),
            conditional("sft", when="build_system=cmake"),
        ),
        default="sft",
        description="CMS for CMS experiment, SFT for ATLAS/LHCb/others.",
    )

    patch("alpgen-214.patch", when="recipe=cms")
    patch("alpgen-214-Darwin-x86_84-gfortran.patch", when="platform=darwin recipe=cms")
    patch("alpgen-2.1.4-sft.patch", when="recipe=sft", level=0)

    def url_for_version(self, version):
        root = self.url.rsplit("/", 2)[0]
        return "{0}/V{1}/v{2}.tgz".format(root, version.up_to(2), version.joined)

    def patch(self):
        if self.spec.satisfies("build_system=cmake"):
            copy(join_path(os.path.dirname(__file__), "CMakeLists.txt"), "CMakeLists.txt")

        if self.spec.satisfies("build_system=makefile"):
            filter_file("-fno-automatic", "-fno-automatic -std=legacy", "compile.mk")
            copy(join_path(os.path.dirname(__file__), "cms_build.sh"), "cms_build.sh")
            copy(join_path(os.path.dirname(__file__), "cms_install.sh"), "cms_install.sh")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    def build(self, pkg, spec, prefix):
        bash = which("bash")
        bash("./cms_build.sh")

    def install(self, pkg, spec, prefix):
        bash = which("bash")
        bash("./cms_install.sh", prefix)

        for root, dirs, files in os.walk(prefix):
            set_install_permissions(root)
            for file in files:
                set_install_permissions(join_path(root, file))
