# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DiamondLinkBottom(Package):
    """Part of diamond-link-{top,left,right,bottom} group"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/diamond-link-bottom-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
