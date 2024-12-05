# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Brillig(Package):
    """Mock package to test the spack versions command."""

    homepage = "https://www.example.com"
    url = "https://github.com/vvolkl/brillig/archive/v2.0.0.tar.gz"

    version("2.0.0", sha256="d4bb8f1737d5a7c0321e1675cceccb59dbcb66a94f3a9dd66a37f58bc6df7f15")
    version("1.0.0", sha256="fcef53f45e82b881af9a6f0530b2732cdaf8c5c60e49b27671594ea658bfe315")
