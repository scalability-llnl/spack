# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sheenbidi(MesonPackage):
    """A sophisticated implementation of Unicode Bidirectional Algorithm"""

    homepage = "https://github.com/Tehreer/SheenBidi"
    url = "https://github.com/Tehreer/SheenBidi/archive/v2.6.tar.gz"
    git = "https://github.com/Tehreer/SheenBidi.git"

    license("Apache-2.0")

    version("2.7", sha256="620f732141fd62354361f921a67ba932c44d94e73f127379a0c73ad40c7fa6e0")
    version("2.6", sha256="f538f51a7861dd95fb9e3f4ad885f39204b5c670867019b5adb7c4b410c8e0d9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
