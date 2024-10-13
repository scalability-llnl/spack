# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aspell6En(AspellDictPackage, GNUMirrorPackage):
    """English (en) dictionary for aspell."""

    homepage = "http://aspell.net/"
    gnu_mirror_path = "aspell/dict/en/aspell6-en-2017.01.22-0.tar.bz2"

    version(
        "2020.12.07-0", sha256="4c8f734a28a088b88bb6481fcf972d0b2c3dc8da944f7673283ce487eac49fb3"
    )
    version(
        "2017.01.22-0", sha256="93c73fae3eab5ea3ca6db3cea8770715a820f1b7d6ea2b932dd66a17f8fd55e1"
    )
