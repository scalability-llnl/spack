# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class CycleB(Package):
    """Package that would lead to cycles if default variant values are used"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/tdep-1.0.tar.gz"

    version("2.0", md5="0123456789abcdef0123456789abcdef")

    variant("cycle", default=True, description="activate cycles")
    depends_on("cycle-a", when="+cycle")
