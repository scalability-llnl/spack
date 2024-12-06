# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Gmake(Package):
    """Simple build tool, with different versions"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/tdep-1.0.tar.gz"

    tags = ["build-tools"]

    version("4.1", md5="0123456789abcdef0123456789abcdef")
    version("4.0", md5="0123456789abcdef0123456789abcdef")
    version("3.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="0123456789abcdef0123456789abcdef")
