# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DepDiamondPatchTop(Package):
    r"""Package that requires a patch on a dependency

  W
 / \
X   Y
 \ /
  Z

    This is package W
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-a-dependency-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    # single patch file in repo
    depends_on("patch", patches="top.patch")
    depends_on("dep-diamond-patch-mid1")
    depends_on("dep-diamond-patch-mid2")
