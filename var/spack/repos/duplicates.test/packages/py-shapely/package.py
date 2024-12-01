# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyShapely(Package):
    """An extension that depends on pinned build dependencies"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/tdep-1.0.tar.gz"

    version("1.25.0", md5="0123456789abcdef0123456789abcdef")

    extends("python")
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("py-setuptools@=60", type="build")
