# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ShellB(Package):
    """Simple package with no dependencies for shell tests"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/shell-b-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("0.9", md5="abcd456789abcdef0123456789abcdef")
