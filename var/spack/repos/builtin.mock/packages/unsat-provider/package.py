# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class UnsatProvider(Package):
    """This package has a dependency on a virtual that cannot be provided"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/v1.0.tgz"

    version("1.0", sha256="0123456789abcdef0123456789abcdef")

    variant("foo", default=True, description="")

    provides("unsatvdep", when="+foo")
    conflicts("+foo")
