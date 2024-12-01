# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Runc(MakefilePackage):
    """CLI tool for spawning containers on Linux according to the OCI specification"""

    homepage = "https://github.com/opencontainers/runc"
    url = "https://github.com/opencontainers/runc/releases/download/v1.0.2/runc.tar.xz"
    maintainers("bernhardkaindl")

    license("Apache-2.0")

    version("1.1.13", sha256="d20e76688ce0681dc687369e18b47aeffcfdac5184c978befa7ce5da35e797fe")
    version("1.1.6", sha256="548506fc1de8f0a4790d8e937eeede17db4beb79c53d66acb4f7ec3edbc31668")
    version("1.1.4", sha256="9f5972715dffb0b2371e4d678c1206cc8c4ec5eb80f2d48755d150bac49be35b")
    version("1.0.2", sha256="740acb49e33eaf4958b5109c85363c1d3900f242d4cab47fbdbefa6f8f3c6909")

    depends_on("c", type="build")  # generated

    depends_on("go", type="build")
    depends_on("go-md2man", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libseccomp")

    def install(self, spec, prefix):
        make("install", "PREFIX=" + prefix)
        symlink(prefix.sbin, prefix.bin)
