# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Patchutils(AutotoolsPackage):
    """This is patchutils, a collection of tools that operate on patch
    files."""

    homepage = "http://cyberelk.net/tim/software/patchutils/"
    url = "http://cyberelk.net/tim/data/patchutils/stable/patchutils-0.4.2.tar.xz"

    license("GPL-2.0-or-later")

    version("0.4.2", sha256="8875b0965fe33de62b890f6cd793be7fafe41a4e552edbf641f1fed5ebbf45ed")
    version("0.4.0", sha256="da6df1fa662b635c2969e7d017e6f32f5b39f1b802673a0af635e4936d4bc2f4")
    version("0.3.4", sha256="cf55d4db83ead41188f5b6be16f60f6b76a87d5db1c42f5459d596e81dabe876")

    depends_on("c", type="build")  # generated
