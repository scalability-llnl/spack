# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cargs(CMakePackage):
    """A lightweight cross-platform C/C++ getopt alternative that works on
    Linux, Windows and macOS."""

    homepage = "https://likle.github.io/cargs/"
    url = "https://github.com/likle/cargs/archive/refs/tags/v1.0.3.tar.gz"
    git = "https://github.com/likle/cargs.git"

    license("MIT")

    version("1.1.0", sha256="87e7da5b539f574d48529870cb0620ef5a244a5ee2eac73cc7559dedc04128ca")
    version("1.0.3", sha256="ddba25bd35e9c6c75bc706c126001b8ce8e084d40ef37050e6aa6963e836eb8b")

    depends_on("c", type="build")  # generated

    depends_on("cmake@3.14.7:", type=("build"))
