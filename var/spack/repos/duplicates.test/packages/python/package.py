# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Python(Package):
    """A package that can be extended"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/tdep-1.0.tar.gz"

    version("3.11.2", md5="0123456789abcdef0123456789abcdef")

    extendable = True

    depends_on("gmake@3", type="build")
