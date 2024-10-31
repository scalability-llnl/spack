# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Earlyoom(MakefilePackage):
    """The oom-killer generally has a bad reputation among Linux users."""

    homepage = "https://github.com/rfjakob/earlyoom"
    url = "https://github.com/rfjakob/earlyoom/archive/v1.6.1.tar.gz"

    license("MIT")

    version("1.8", sha256="bbb050a2294e60dafc0b129fcec705ef95d9d27f4c9dae1d3b4f25e4f698ae41")
    version("1.6.1", sha256="bcd3fab4da5e1dddec952a0974c866ec90c5f9159c995f9162c45488c4d03340")
    version("1.6", sha256="b81804fc4470f996014d52252a87a1cf3b43d3d8754140035b10dcee349302b8")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("earlyoom", prefix.bin)
