# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cubature(CMakePackage):
    """multi-dimensional adaptive integration (cubature) in C"""

    url = "https://github.com/stevengj/cubature/archive/refs/tags/v1.0.4.tar.gz"
    git = "https://github.com/stevengj/cubature"

    license("GPL-2")

    version("1.0.4", sha256="cd4899de0b047a9d220cfb751a8bdbb8fd0c97c1c894d07523b75168e6426f60")
