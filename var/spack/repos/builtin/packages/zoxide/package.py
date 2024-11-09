# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zoxide(CargoPackage):
    """zoxide is a smarter cd command, inspired by z and autojump. It
    remembers which directories you use most frequently, so you can
    "jump" to them in just a few keystrokes. zoxide works on all major shells.
    """

    homepage = "https://github.com/ajeetdsouza/zoxide"
    url = "https://github.com/ajeetdsouza/zoxide/archive/refs/tags/v0.9.4.tar.gz"

    maintainers("pranav-sivaraman")

    license("MIT")

    version("0.9.6", sha256="e1811511a4a9caafa18b7d1505147d4328b39f6ec88b88097fe0dad59919f19c")
    version("0.9.5", sha256="1278660e671d96c5421f0910fa7d79b9e0bb0bfacf7611ff63bf383f721d7a4f")
    version("0.9.4", sha256="ec002bdca37917130ae34e733eb29d4baa03b130c4b11456d630a01a938e0187")
