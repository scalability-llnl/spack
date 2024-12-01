# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ConflictingDependent(Package):
    """By itself this package does not have conflicts, but it is used to
    ensure that if a user tries to build with an installed instance
    of dependency-install@2 that there is a failure."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("dependency-install@:1.0")
