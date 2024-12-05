# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aspell6De(AspellDictPackage, GNUMirrorPackage):
    """German (de) dictionary for aspell."""

    homepage = "http://aspell.net/"
    gnu_mirror_path = "aspell/dict/de/aspell6-de-20030222-1.tar.bz2"

    license("GPL-2.0-or-later")

    version(
        "6-de-20161207-7-0",
        sha256="c2125d1fafb1d4effbe6c88d4e9127db59da9ed92639c7cbaeae1b7337655571",
    )
    version(
        "6-de-20030222-1",
        sha256="ba6c94e11bc2e0e6e43ce0f7822c5bba5ca5ac77129ef90c190b33632416e906",
    )
