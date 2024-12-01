# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyExtension3(Package):
    """Package with a dependency whose presence is conditional to the
    version of Python being used.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/extension3-1.0.tar.gz"

    depends_on("python")
    depends_on("py-extension1", type=("build", "run"), when="^python@:2.8.0")

    depends_on("patchelf@0.9", when="@1.0:1.1 ^python@:2")
    depends_on("patchelf@0.10", when="@1.0:1.1 ^python@3:")

    version("2.0", md5="00000000000000000000000000000320")
    version("1.1", md5="00000000000000000000000000000311")
    version("1.0", md5="00000000000000000000000000000310")
