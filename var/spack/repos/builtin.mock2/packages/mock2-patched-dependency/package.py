# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mock2PatchedDependency(Package):
    """Package patched by patch-a-foreign-dependency in builtin.mock."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/mock2-patch-dependency-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
