# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AbiComplianceChecker(MakefilePackage):
    """A tool for checking backward compatibility of a C/C++ library API."""

    homepage = "https://github.com/lvc/abi-compliance-checker"
    url = "https://github.com/lvc/abi-compliance-checker/archive/2.3.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.3", sha256="b1e32a484211ec05d7f265ab4d2c1c52dcdb610708cb3f74d8aaeb7fe9685d64")
    version("2.2", sha256="9fb7b17e33d49e301d02a6374fbd2596feb53ecc77194879a4e1c2d1e24b4ddb")
    version("2.1", sha256="0e19ea16b6c6aa6c7b222063127427bef3b835adbbd9e6606a972a912599d014")

    depends_on("abi-dumper@1.1:")
    depends_on("perl@5:")
    depends_on("binutils")
    depends_on("universal-ctags")

    def install(self, spec, prefix):
        make(f"prefix={prefix}", "install")
