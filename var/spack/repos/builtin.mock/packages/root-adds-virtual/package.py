# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RootAddsVirtual(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/root-adds-virtual-1.0.tar.gz"

    version("1.0", sha256="abcdef0123456789abcdef0123456789")

    depends_on("middle-adds-virtual")
