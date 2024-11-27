# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mcutils(MakefilePackage):
    """A collection of routines for classification and manipulation of
    particle physics simulated HepMC event records."""

    homepage = "https://gitlab.com/hepcedar/mcutils"
    git = "https://gitlab.com/hepcedar/mcutils.git"

    tags = ["hep"]

    license("GPL-3.0-or-later")

    version("1.3.5", tag="mcutils-1.3.5", commit="d0e65bb7b6f80d6df50a71a25c54683b0db997a5")
    version("1.3.4", tag="mcutils-1.3.4", commit="ddb527e5d03b8e4d13ae4e6d78fbcd7d35f7153b")
    version("1.3.3", tag="mcutils-1.3.3", commit="638aabe930b05f8ecfe272bdd2f2a7ed65e5fc45")
    version("1.3.2", tag="mcutils-1.3.2", commit="8228d443aa0877c067299d640704836e664dac51")
    version("1.3.1", tag="mcutils-1.3.1")
    version("1.3.1", tag="mcutils-1.3.0", commit="e04693bf5aaa38b9cbe76aec94a3ffd2d466f1f6")
    version("1.2.1", tag="mcutils-1.2.1", commit="3799336668c19ed86c93c82c815da6397597763f")
    version("1.2.0", tag="mcutils-1.2.0", commit="c1ef0a2a0b09c9df16450c7b64da543119e3740f")
    version("1.1.2", tag="mcutils-1.1.2", commit="cf212f61bb398cae1e987ff7e4c5537c1480be8d")
    version("1.1.1", tag="mcutils-1.1.1", commit="c42d9123439fbcee512c23f853c60d6491b47fa0")
    version("1.1.0", tag="mcutils-1.1.0", commit="15af9f40d8667030d9a68e007ac7e348157397d5")
    version("1.0.3", tag="mcutils-1.0.3", commit="73a8e06256460e943af2336f80115d84630f6dd5")
    version("1.0.2", tag="mcutils-1.0.2", commit="15e2daad2bfe7543e43b35421fffd177519c516f")
    version("1.0.1", tag="mcutils-1.0.1", commit="85bb1c9e2761a7c70bdd18955d6cccc120d9c523")
    version("1.0.0", tag="mcutils-1.0.0", commit="7ae9d007493ce65f5eac432d0ea6f730512a0a8a")

    depends_on("cxx", type="build")  # generated

    depends_on("heputils", when="@1.1.0:")

    def install(self, spec, prefix):
        make("install", "PREFIX={0}".format(prefix))
