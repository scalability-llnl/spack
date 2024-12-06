# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PySetuptools(Package):
    """Build tool for an extendable package"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/tdep-1.0.tar.gz"

    tags = ["build-tools"]

    extends("python")

    version("60", md5="0123456789abcdef0123456789abcdef")
    version("59", md5="0123456789abcdef0123456789abcdef")
