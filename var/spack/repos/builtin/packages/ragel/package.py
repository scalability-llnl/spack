# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ragel(AutotoolsPackage):
    """Ragel State Machine Compiler
    Ragel compiles executable finite state machines from regular
    languages. Ragel targets C, C++ and ASM. Ragel state machines can
    not only recognize byte sequences as regular expression machines
    do, but can also execute code at arbitrary points in the
    recognition of a regular language. Code embedding is done using
    inline operators that do not disrupt the regular language syntax.
    """

    homepage = "https://www.colm.net/open-source/ragel"
    git = "git://colm.net/ragel.git"
    url = "https://www.colm.net/files/ragel/ragel-6.10.tar.gz"

    license("GPL-2.0-or-later")

    version("6.10", sha256="5f156edb65d20b856d638dd9ee2dfb43285914d9aa2b6ec779dac0270cd56c3f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("colm", type="build")
