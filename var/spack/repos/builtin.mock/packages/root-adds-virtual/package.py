# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RootAddsVirtual(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/root-adds-virtual-1.0.tar.gz"

    version("1.0", sha256="abcdef0123456789abcdef0123456789")

    depends_on("middle-adds-virtual")
