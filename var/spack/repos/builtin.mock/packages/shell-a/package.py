# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ShellA(Package):
    """Simple package with one dependency for shell tests"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/shell-a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="abcdef0123456789abcdef0123456789")

    depends_on("shell-b")
