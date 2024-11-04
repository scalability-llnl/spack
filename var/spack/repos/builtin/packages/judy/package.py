# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Judy(AutotoolsPackage):
    """Judy: General-purpose dynamic array, associative array and hash-trie."""

    homepage = "https://judy.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/judy/judy/Judy-1.0.5/Judy-1.0.5.tar.gz"

    license("LGPL-2.0-only")

    version("1.0.5", sha256="d2704089f85fdb6f2cd7e77be21170ced4b4375c03ef1ad4cf1075bd414a63eb")

    depends_on("c", type="build")  # generated

    parallel = False
